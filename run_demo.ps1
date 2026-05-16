# Fish Behavior Tracking System - Complete Demo Runner (PowerShell)
# Automates the entire demo pipeline

$PYTHON = "c:/Users/kowne/AppData/Local/Python/pythoncore-3.14-64/python.exe"
$ErrorActionPreference = "Stop"

function Print-Header {
    param([string]$Title)
    Write-Host "`n$('='*60)" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "$('='*60)" -ForegroundColor Cyan
}

function Run-Command {
    param(
        [string[]]$Command,
        [string]$StepName
    )
    
    Write-Host "`n[$StepName] Running: $($Command -join ' ')"
    Write-Host "$('-'*60)"
    
    try {
        & $Command[0] $Command[1..($Command.Length-1)]
        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ $StepName failed with exit code $LASTEXITCODE" -ForegroundColor Red
            return $false
        }
        return $true
    }
    catch {
        Write-Host "✗ $StepName failed: $_" -ForegroundColor Red
        return $false
    }
}

# Main execution
try {
    Print-Header "Fish Behavior Tracking System - Complete Demo"
    
    # Step 1: Verify Dependencies
    if (-not (Run-Command @($PYTHON, "test_dependencies.py") "STEP 1/3: Verify Dependencies")) {
        exit 1
    }
    
    # Step 2: Generate Demo Data
    if (-not (Run-Command @($PYTHON, "demo_setup.py") "STEP 2/3: Generate Demo Data")) {
        exit 1
    }
    
    # Step 3: Run Tracker
    if (-not (Run-Command @(
        $PYTHON, "deep_sort_app.py",
        "--sequence_dir", "demo_data/sequences/test_sequence",
        "--detection_file", "demo_data/sequences/detections.npy",
        "--output_file", "demo_output.txt",
        "--display", "False"
    ) "STEP 3/3: Run DeepSORT Tracker")) {
        exit 1
    }
    
    # Display Results
    Print-Header "Tracking Results"
    
    $outputFile = "demo_output.txt"
    if (-not (Test-Path $outputFile)) {
        Write-Host "✗ Output file not found!" -ForegroundColor Red
        exit 1
    }
    
    $lines = Get-Content $outputFile
    if ($lines -is [string]) { $lines = @($lines) }
    
    # Display first 10 results
    Write-Host "`nFirst 10 tracking results:" -ForegroundColor Green
    Write-Host "$('-'*60)"
    $lines[0..9] | ForEach-Object {
        Write-Host "  $_"
    }
    
    # Display last 5 results
    if ($lines.Length -gt 10) {
        Write-Host "`nLast 5 tracking results:" -ForegroundColor Green
        Write-Host "$('-'*60)"
        $lines[-5..-1] | ForEach-Object {
            Write-Host "  $_"
        }
    }
    
    # Statistics
    Write-Host "`n$('-'*60)"
    Write-Host "Total tracked detections: $($lines.Length)" -ForegroundColor Yellow
    
    $fileSize = (Get-Item $outputFile).Length
    Write-Host "Output file size: $($fileSize:N0) bytes" -ForegroundColor Yellow
    
    # Summary
    Print-Header "Summary"
    Write-Host @"

✓ Demo run completed successfully!

Next Steps:
  1. Review tracking results in: demo_output.txt
  
  2. Request real fish video dataset:
     https://docs.google.com/forms/d/...
  
  3. Place video sequences in: demo_data/sequences/
  
  4. Run tracker on real data:
     python deep_sort_app.py `
       --sequence_dir demo_data/sequences/fish_video_1 `
       --detection_file detections.npy `
       --output_file results.txt

System Features:
  • Multi-object tracking with DeepSORT
  • Appearance-based identity maintenance
  • Kalman filter motion prediction
  • MOTChallenge-format output
  
For more information, see: SETUP_COMPLETE.md

"@ -ForegroundColor Green
    
    Write-Host "$('='*60)`n" -ForegroundColor Cyan
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
