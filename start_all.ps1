# 启动前端 (Vue3 + Vite)
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "d:\firstlove\11\frontend"
    npm run dev 2>&1 | Out-File -FilePath "d:\firstlove\11\frontend.log" -Append
} -Name "frontend"

Start-Sleep -Seconds 5

# 输出前端日志以确认启动
Get-Content "d:\firstlove\11\frontend.log" -Tail 20

Write-Host ""
Write-Host "=== 启动完成 ==="
Write-Host "后端服务: http://localhost:8000"
Write-Host "前端服务: http://localhost:5173 (或查看上方日志中的端口)"
Write-Host ""
Write-Host "测试命令: python d:\firstlove\11\test_project.py"
