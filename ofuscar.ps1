$src = "static_src\js"
$dst = "static\js"

if (!(Test-Path $dst)) { New-Item -ItemType Directory -Path $dst -Force }

Get-ChildItem -Path $src -Filter *.js | ForEach-Object {
    $input = $_.FullName
    $output = Join-Path $dst $_.Name

    javascript-obfuscator $input --output $output `
        --compact true `
        --control-flow-flattening true `
        --control-flow-flattening-threshold 0.75 `
        --dead-code-injection true `
        --dead-code-injection-threshold 0.4 `
        --string-array true `
        --string-array-encoding base64 `
        --string-array-rotate true `
        --string-array-shuffle true `
        --string-array-threshold 0.75 `
        --identifier-names-generator hexadecimal `
        --numbers-to-expressions true `
        --self-defending true `
        --disable-console-output true `
        --debug-protection true `
        --debug-protection-interval 4000 `
        --target browser

    Write-Host "Ofuscado: $($_.Name)"
}