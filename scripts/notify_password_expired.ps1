$PSEmailServer = 'mail.rossiya-airlines.com'
$temp
$mail=$temp
$ExpireDays=$temp
$mail =(Get-ADUser -identity "99286" -Properties EmailAddress).EmailAddress 
$encoding = [System.Text.Encoding]::UTF8
$ExpireDate=$temp
$PasswdSetDate=(Get-ADUser -identity "RU99286" -Property PasswordLastSet).PasswordLastSet
$mail
$new 
$MaxPasswdAge = (Get-ADDefaultDomainPasswordPolicy).MaxPasswordAge 
$ExpireDate
$ExpireDate = $PasswdSetDate + $MaxPasswdAge
#100 дней
$Today = (get-date)
$DaysToExpire = (New-TimeSpan -Start $Today -End $ExpireDate).Days
Send-MailMessage -From 'gse@rossiya-airlines.com' -To $mail -Subject 'Истекает пароль удаленного доступа' -Body ("Дней до истечения пароля удаленного доступа: " + $DaysToExpire + " Просьба сменить пароль."  | Out-String) -Encoding $encoding
