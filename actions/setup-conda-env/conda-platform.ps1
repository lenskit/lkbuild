<#
.DESCRIPTION
conda-platform obtains the Anaconda platform string.
#>


# Add the conda bin directory to PATH if it exists
if ($env:CONDA) {
    $conda_bin = Join-Path $env:CONDA 'condabin'
    $psep = [IO.Path]::PathSeparator
    $env:PATH = "$conda_bin$psep$env:PATH"
}

# Get and parse the conda info string
$info_str = (conda info --json |Join-String)
$info = (ConvertFrom-Json $info_str)
$plat = $info.platform

# Extract platform and write it
Write-Host "::set-output name=platform::$plat"

# Copy boot file
if ($env:ACTION_PATH) {
    $lockfile = (Join-Path $env:ACTION_PATH "conda-$plat.lock")
    Write-Host "::set-output name=lock-file::bootstrap-$plat.lock"
    Copy-Item -Force $lockfile "bootstrap-$plat.lock"
}
