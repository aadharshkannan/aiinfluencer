# Path to the file containing quotes (one per line)
$quoteFile = "quotes.txt"

# Ensure the file exists
if (-Not (Test-Path $quoteFile)) {
    Write-Error "Quote file not found: $quoteFile"
    exit 1
}

# Read all quotes
$quotes = Get-Content $quoteFile

# Loop through each quote
foreach ($quote in $quotes) {
    try {
        Write-Output "Processing: $quote"
        & python main.py "`"$quote`""
    }
    catch {
        Write-Warning "Failed to process quote: $quote"
        Write-Warning $_.Exception.Message
    }
}