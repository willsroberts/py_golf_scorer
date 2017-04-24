# py_golf_scorer
Py Library For Updating Google Doc

#1 Intent:
This library is for updating a google sheet with the scores of the current tournament being plaid.
Within the sheet, there are a plethora of actions available for execution on data. The intent of
the library is for gathering the information from the relevant players specified by the user.

This library relies upon the client for updating google drive items via python available here:
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
If one is to use this py_golf_score, they would need to follow the steps above to authorize a
sheet for the client to use.

The usage of this library is great for individuals interested in bestball and net
gaming for professional tournaments.  

#2 Usage:
1. Create google sheets doc
  1. Name google doc
  1. For net scoring
    1. Name sheet "Scores"
    1. Add golfers name in separate rows
  1. For best ball scoring
    1. Name sheets by round: "round_1","round_2", "round_3", "round_4"
    1. Add golfers names in separate rows
2. Command Line Steps
  2. `git clone`
  2. `cp <downloads>/client_secret.json ./config/``
  2. `python <-i> score_updater.py "<google_doc_name>" '<golfer_1' 'golfer_2' 'golfer_3' 'golfer_4'``
  2. confirm scores updated where available in google doc

#3 Considerations
This library is dependent upon the leaderboard published on pgatour.com/leaderboard.html. Future iterations
will plan for the ability of the user to specify which source they want to scrape from: pgatour.com/espn.go.com/
in case of pgatour.com's leaderboard malfunction etc.

Please feel free to email with question!
