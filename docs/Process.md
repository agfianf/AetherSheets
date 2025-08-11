
Register all we need:

## Spreadsheet Configuration

To access spreadsheets via Google Sheets API you need to authenticate and authorize your application.
- If you plan to access spreadsheets on behalf of a bot account use Service Account.
- If you’d like to access spreadsheets on behalf of end users (including yourself) use OAuth Client ID.
- If you’d like to only open public spreadsheets use API key

### Enable API Access for a Project

1. Head to Google Developers Console and create a new project (or select the one you already have).
2. In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
3. In the box labeled “Search for APIs and Services”, search for “Google Sheets API” and enable it.

### For Bots: Using Service Account
A service account is a special type of Google account intended to represent a non-human user that needs to authenticate and be authorized to access data in Google APIs [sic].

Since it’s a separate account, by default it does not have access to any spreadsheet until you share it with this account. Just like any other Google account.

- Enable API Access for a Project if you haven’t done it yet.
- Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
- Fill out the form
- Click “Create” and “Done”.
- Press “Manage service accounts” above Service Accounts.
- Press on ⋮ near recently created service account and select “Manage keys” and then click on “ADD KEY > Create new key”.
- Select JSON key type and press “Create”.