$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir
try {
    $oldTexInputs = $env:TEXINPUTS
    $env:TEXINPUTS = ".\tum//;" + $oldTexInputs

    pdflatex -interaction=nonstopmode main.tex
    bibtex main
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex
}
finally {
    $env:TEXINPUTS = $oldTexInputs
    Pop-Location
}
