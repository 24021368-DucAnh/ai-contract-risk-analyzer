# Read source contracts through Word without changing the original files.
# Requires Microsoft Word on Windows. Output uses UTF-8 without BOM.
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceDir = Join-Path $repoRoot 'data\raw\contracts'
$outputDir = Join-Path $repoRoot 'data\processed\raw_text'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
$wordApp.AutomationSecurity = 3
try {
    Get-ChildItem $sourceDir -File | ForEach-Object {
        $document = $wordApp.Documents.Open($_.FullName, $false, $true)
        try {
            $text = $document.Content.Text.Replace("`r", "`n").Replace([char]7, ' ').Replace([char]11, ' ')
            $text = [regex]::Replace($text, '[^\S\n]+(?=\n|$)', '').TrimEnd()
            $output = Join-Path $outputDir ($_.BaseName + '.txt')
            [System.IO.File]::WriteAllText($output, $text, [System.Text.UTF8Encoding]::new($false))
            Write-Output "Extracted $($_.Name) -> $output"
        }
        finally {
            $document.Close(0)
        }
    }
}
finally {
    $wordApp.Quit()
}
