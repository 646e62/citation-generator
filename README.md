# citation-detector

## The project

### Overview

This app generates legal citations. Although the app's initial focus will be on getting McGill-correct citations, the end goal will be to code rules that will comply with all major Canadian courts and jurisdictions.

### Inspiration

When I started law school, a developer started a project that took a website URL — specifically, a link to a reported case on CanLII — and converted it to a McGill-correct citation. Every first year law student has better things to worry about than citations, and I was no exception. More than once, I felt that this website was a lifesaver, as it allowed me to focus on substantive, complex concerns while an algorithm or two made the citation process virtually automatic.

Unfortunately, the web app I used shut down just a few months before I finished law school. While I'd had plenty of time to figure out how to do correct citations, and very often with the website's help, the app's disappearance left an obvious gap in the workflow I'd become accustomed to. To my knowledge, nothing has replaced it. At least, nothing remotely affordable. This app aims to fill that gap.

## What problem does this address?

Legal work lives and dies around documents. Even for so-called "trial lawyers" like myself who spend most of their work day in court, an inordinate amount of time is spent drafting documents for clients, judges, and other lawyers. Where this drafting includes references to other works, legal citations come into play. In a common law system like Canada's, where the concept of *precedent* is key, most written legal work involves frequent references to previous binding decisions and other authoritative texts. 

Not every law school professor, legal office, or senior/supervising partner will care about correct citations. But enough of them will and do to make an app like this worthwhile. Correctly citing various sources in legal documents can be tricky, tedious, and incredibly time consuming. Having this process automated while I was in law school was a lifesaver, and although I don't rely on citations as much as I used to, having this process automated once again will greatly improve my workflow. I expect that there are many others in my situation who would feel similarly.

## What are a legal citation's components?

### Case

* Style of cause
* Neutral citation
* Print reporter
* Pinpoint

## Who has the data?

### McGill Guide to Uniform Legal Citations

The "McGill Guide" is the go-to source for most legal citations in Canada. This book contains both rules for citations and abbreviations for myriad journals, courts, and case reporters. Where provincial rules don't outline a rule or a correct citation, the forms and rules that the McGill Guide outlines are usually the default. Therefore, it is arguably the app's most critical data component.

### CanLII

CanLII is a free and accessible database of Canadian legal decisions, statutes, and journal articles. It is non-profit and funded by Canadian Law Societies. It is my leading source for case law and statutes in practice, and will very likely be the leading source for this material in this project.

### Westlaw, Quicklaw, HeinOnline and other proprietary sources

Proprietary sources are unlikely to be a good source of data, despite being widely available to lawyers and law students. Companies like Thompson Reuters and LexisNexis offer their own comparable (albeit incredibly expensive) services and aren't likely to play nice. HeinOnline is much smaller but still appears to be a closed ecosystem.

