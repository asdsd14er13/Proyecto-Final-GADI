$docxPath = (Resolve-Path "Primer_Entregable_GADI_UNFV.docx").Path
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
Write-Host "Iniciando exportación de Word a PDF..."
Write-Host "Origen: $docxPath"
Write-Host "Destino: $pdfPath"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    $wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)
    $doc.Close()
    Write-Host "EXPORT_STATUS: SUCCESS"
}
catch {
    Write-Error $_
}
finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
