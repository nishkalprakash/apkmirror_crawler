**This Repo is to crawl the entire apkmirror site to get all apks and store in Google Drive**

_Credentials are redacted_

---
* There is a dependance on MongoDB (for fetching jobs and keeping track)...
* The code runs asyncronously utilizing maximum resources available...
* The inherent rate limit after trial and error (a lot of 15 min bans, :p) turned out to be 1req/s to fetch from apkmirror and 1req/s to direct push to goolge drive
* To crawl the entire space of 1million, we would need ~11.55 days...
* The main driver code is in apk_rclone.py