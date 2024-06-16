
$WorkingPath = Read-Host "Enter Project Reality Repo Directory"
while (-not @(Test-Path $WorkingPath -PathType Container)) {
    $WorkingPath = Read-Host "Incorrect directory. Enter directory"
}
Set-Location -Path $WorkingPath
