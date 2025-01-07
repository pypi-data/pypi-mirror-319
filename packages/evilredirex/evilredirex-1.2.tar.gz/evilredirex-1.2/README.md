EvilRedirex
 
EvilRedirex is a Python tool designed by EvilTwinz(SrilakiVarma) for detecting open redirects and XSS vulnerabilities in web applications. It automates vulnerability scanning by testing URLs with various payloads to identify exploitable parameters.
Features
 
    Open Redirect Detection: Identifies URLs vulnerable to open redirects.
    XSS Vulnerability Detection: Detects parameters susceptible to cross-site scripting (XSS) attacks.
    Threaded Scanning: Processes multiple tests simultaneously for faster results.
    Selenium Integration: Uses a headless browser for advanced vulnerability detection.
 
Installation
 
    pip install evilredirex
 
Usage
Command-Line Options
evilredirex --help
 
Example Usage:

    1.Test a single URL:
            evilredirex -u "http://example.com"
    2.Test URLs from a file:
            cat urls.txt | evilredirex
    3.Silent mode:
            evilredirex -u "http://example.com" --silent
 
 
Requirements
 
Ensure the following are installed on your system:
 
    Python 3.6+
    ChromeDriver
    Required Python libraries (automatically installed with pip install evilredirex).