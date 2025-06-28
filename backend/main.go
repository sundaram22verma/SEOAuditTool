package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"

	colly "github.com/gocolly/colly/v2"
)

type PageReport struct {
	URL         string   `json:"url"`
	Title       string   `json:"title"`
	MetaDesc    string   `json:"meta_description"`
	Headings    []string `json:"headings"`
	BrokenLinks []string `json:"broken_links"`
}

type AuditReport struct {
	Pages []PageReport `json:"pages"`
}

func isAbsoluteURL(link string) bool {
	return strings.HasPrefix(link, "http://") || strings.HasPrefix(link, "https://")
}

func main() {
	var file string
	flag.StringVar(&file, "file", "", "Path to .txt file with URLs (one per line)")
	flag.Parse()

	urls := flag.Args()

	if file != "" {
		data, err := ioutil.ReadFile(file)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
			os.Exit(1)
		}
		lines := strings.Split(string(data), "\n")
		for _, line := range lines {
			line = strings.TrimSpace(line)
			if line != "" {
				urls = append(urls, line)
			}
		}
	}

	if len(urls) == 0 {
		fmt.Println("No URLs provided.")
		os.Exit(1)
	}

	report := AuditReport{}
	for _, u := range urls {
		page := PageReport{
			URL:         u,
			Title:       "",
			MetaDesc:    "",
			Headings:    []string{},
			BrokenLinks: []string{},
		}
		c := colly.NewCollector()

		c.OnHTML("title", func(e *colly.HTMLElement) {
			page.Title = e.Text
		})
		c.OnHTML("meta[name='description']", func(e *colly.HTMLElement) {
			page.MetaDesc = e.Attr("content")
		})
		for _, h := range []string{"h1", "h2", "h3", "h4", "h5", "h6"} {
			h := h // capture range variable
			c.OnHTML(h, func(e *colly.HTMLElement) {
				txt := strings.TrimSpace(e.Text)
				if txt != "" {
					page.Headings = append(page.Headings, strings.ToUpper(h)+": "+txt)
				}
			})
		}

		var links []string
		c.OnHTML("a[href]", func(e *colly.HTMLElement) {
			href := e.Attr("href")
			if isAbsoluteURL(href) {
				links = append(links, href)
			} else if strings.HasPrefix(href, "/") {
				// Use net/url to resolve relative URLs correctly
				baseURL, err := url.Parse(u)
				if err == nil {
					rel, err := url.Parse(href)
					if err == nil {
						abs := baseURL.ResolveReference(rel)
						links = append(links, abs.String())
					}
				}
			}
		})

		err := c.Visit(u)
		if err != nil {
			page.Title = "[ERROR] Could not fetch page"
		}

		// Check links for broken status
		client := &http.Client{Timeout: 5 * time.Second}
		for _, link := range links {
			resp, err := client.Head(link)
			if err != nil || resp.StatusCode >= 400 {
				status := 0
				if resp != nil {
					status = resp.StatusCode
				}
				errMsg := ""
				if err != nil {
					errMsg = err.Error()
				}
				brokenInfo := link + " [status: " + fmt.Sprint(status) + "]"
				if errMsg != "" {
					brokenInfo += " [error: " + errMsg + "]"
				}
				page.BrokenLinks = append(page.BrokenLinks, brokenInfo)
			}
			if resp != nil {
				resp.Body.Close()
			}
		}

		report.Pages = append(report.Pages, page)
	}

	// Get the shared directory path from environment or use default
	sharedDir := os.Getenv("SHARED_DIR")
	if sharedDir == "" {
		// Default to ../shared relative to current working directory
		sharedDir = filepath.Join("..", "shared")
	}

	os.MkdirAll(sharedDir, 0755)
	reportPath := filepath.Join(sharedDir, "report.json")
	f, err := os.Create(reportPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating report: %v\n", err)
		os.Exit(1)
	}
	defer f.Close()
	enc := json.NewEncoder(f)
	enc.SetIndent("", "  ")
	if err := enc.Encode(report); err != nil {
		fmt.Fprintf(os.Stderr, "Error writing report: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Report generated at", reportPath)
}
