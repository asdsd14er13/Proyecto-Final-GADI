$docxPath = (Resolve-Path "NUEVO_PAPER_PROYECTO_GADI.docx").Path
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
Write-Host "Exportando $docxPath a PDF..."

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

# Crear copia con espacios también para el PDF
Copy-Item $pdfPath "NUEVO PAPER PROYECTO GADI.pdf" -Force
Write-Host "Archivos generados:"
Write-Host "- NUEVO_PAPER_PROYECTO_GADI.docx"
Write-Host "- NUEVO_PAPER_PROYECTO_GADI.pdf"
Write-Host "- NUEVO PAPER PROYECTO GADI.docx"
Write-Host "- NUEVO PAPER PROYECTO GADI.pdf"
