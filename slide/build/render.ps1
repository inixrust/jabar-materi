# Render slide PPTX ke PNG memakai PowerPoint (pengganti soffice + pdftoppm di Windows).
# Pemakaian: powershell -File render.ps1 <deck.pptx> <outdir> [lebar_px] [nomor_slide,...]
param([string]$Deck, [string]$Out, [int]$Width = 960, [string]$Only = '')
$ErrorActionPreference = 'Stop'
$Deck = (Resolve-Path $Deck).Path
New-Item -ItemType Directory -Force $Out | Out-Null
$Out = (Resolve-Path $Out).Path
$h = [int]($Width * 9 / 16)
$pp = New-Object -ComObject PowerPoint.Application
try {
    $pres = $pp.Presentations.Open($Deck, $true, $false, $false)
    $want = @()
    if ($Only) { $want = $Only.Split(',') | ForEach-Object { [int]$_ } }
    $base = [IO.Path]::GetFileNameWithoutExtension($Deck)
    for ($i = 1; $i -le $pres.Slides.Count; $i++) {
        if ($want.Count -gt 0 -and -not ($want -contains $i)) { continue }
        $f = Join-Path $Out ('{0}_{1:D3}.png' -f $base, $i)
        $pres.Slides.Item($i).Export($f, 'PNG', $Width, $h)
    }
    $pres.Close()
} finally {
    $pp.Quit() | Out-Null
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null
}
