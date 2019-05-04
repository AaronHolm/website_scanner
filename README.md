# website_scanner
Check a webpage to determine if the page has changed

Code adapted from Hunter Thornsberry's example in http://adventuresintechland.com/detect-when-a-webpage-changes-with-python

With a SQL table that has the name of a webpage, a link to that webpage and stored hash of what the page was like when last checked,
this script will check that page again, create a new hash and compare the two to determine if any changes have been made therein.

If changes have been made, then send an email to run any ETL or other scripts.
