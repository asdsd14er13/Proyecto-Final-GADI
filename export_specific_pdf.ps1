$docxPath = (Resolve-Path "03_INFORME_FASE_1_CAPITULOS_I_Y_II.docx").Path
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, ".pdf")
Write-Host "Iniciando exportación de $docxPath a PDF..."

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

# Copiar también a la carpeta DOCUMENTACION/guias_internas/
$destFolder = "DOCUMENTACION\guias_internas"
Copy-Item $docxPath (Join-Path $destFolder "03_INFORME_FASE_1_CAPITULOS_I_Y_II.docx") -Force
Copy-Item $pdfPath (Join-Path $destFolder "03_INFORME_FASE_1_CAPITULOS_I_Y_II.pdf") -Force
Write-Host "Archivos replicados con éxito en $destFolder"
