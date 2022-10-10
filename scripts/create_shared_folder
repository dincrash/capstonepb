#запускать с сервера где есть модуль FSRM
#$pathIFS = Read-host "Директория папки \\vm-ifs05\E$\Shares"
"создает в stc.local\otdel\*"
$Name = Read-host "Имя папки"
$GB = Read-host "Квота лимит (2,5,10,50,100)"
$NameRO=$Name+"_RO"
$NameRW=$Name+"_RW"
#description change
$path="\\stc.local\otdel\"+$Name
$pathIFS="\\vm-ifs05\E`$\Shares\Otdel\"+$Name
new-item $pathIFS -itemtype directory
#add -Description $path
New-ADGroup -Name $NameRW -SamAccountName $NameRW -GroupCategory Security -GroupScope Global -DisplayName $NameRW -Path "OU=Группы на диски отделов,OU=Группы с правами на серверах,DC=stc,DC=local" -Description $path
New-ADGroup -Name $NameRO -SamAccountName $NameRO -GroupCategory Security -GroupScope Global -DisplayName $NameRO -Path "OU=Группы на диски отделов,OU=Группы с правами на серверах,DC=stc,DC=local" -Description $path



$AuditUser = "kvi"
$AuditRules = "Delete,DeleteSubdirectoriesAndFiles,CreateFiles,AppendData,ExecuteFile,ReadData"
$InheritType = "ContainerInherit,ObjectInherit"
$AuditType = "Success"
$AccessRule = New-Object System.Security.AccessControl.FileSystemAuditRule($AuditUser,$AuditRules,$InheritType,"None",$AuditType)
$ACL = (get-item $pathIFS).GetAccessControl('Access')
$acl.SetAccessRuleProtection($true, $true)
$ACL.SetAuditRuleProtection($false, $false)
$ACL.SetAuditRule($AccessRule)
$ACL | Set-Acl $pathIFS
$ACL = Get-Acl $pathIFS -Audit
$ACL.RemoveAuditRule($AccessRule)
$ACL | Set-Acl -Path $pathIFS

#уменьшить добавить форич для каждого параметра objuser

$colRights = [System.Security.AccessControl.FileSystemRights] "FullControl" 
$InheritanceFlag = [System.Security.AccessControl.InheritanceFlags]::None
$PropagationFlag = [System.Security.AccessControl.PropagationFlags]::None 
$objType = [System.Security.AccessControl.AccessControlType]::Allow 
$objUser = New-Object System.Security.Principal.SecurityIdentifier("S-1-5-18") 
$objACE = New-Object System.Security.AccessControl.FileSystemAccessRule($objUser, $colRights, $InheritanceFlag, $PropagationFlag, $objType) 
$objACL = Get-Acl $pathIFS 
$objACL.RemoveAccessRuleAll($objACE) 
Set-Acl $pathIFS $objACL

#добавляет права RO RW
$rb=(Get-ADGroup -Identity $NameRO).SID
$Acl = Get-Acl $pathIFS
$Ar = New-Object System.Security.AccessControl.FileSystemAccessRule($rb , "ReadAndExecute", "ContainerInherit,ObjectInherit", "None", "Allow")
$Acl.SetAccessRule($Ar)
Set-Acl $pathIFS $Acl

$rb=(Get-ADGroup -Identity $NameRW).SID
$Acl = Get-Acl $pathIFS
$Ar = New-Object System.Security.AccessControl.FileSystemAccessRule($rb , "Modify", "ContainerInherit,ObjectInherit", "None", "Allow")
$Acl.SetAccessRule($Ar)
Set-Acl $pathIFS $Acl






$objUser = New-Object System.Security.Principal.SecurityIdentifier("S-1-5-21-3232868440-3454693121-3805172430-17216") 
$objACE = New-Object System.Security.AccessControl.FileSystemAccessRule($objUser, $colRights, $InheritanceFlag, $PropagationFlag, $objType) 
$objACL = Get-Acl $pathIFS
$objACL.RemoveAccessRuleAll($objACE) 
Set-Acl $pathIFS $objACL

$objUser = New-Object System.Security.Principal.SecurityIdentifier("S-1-5-21-3232868440-3454693121-3805172430-513") 
$objACE = New-Object System.Security.AccessControl.FileSystemAccessRule($objUser, $colRights, $InheritanceFlag, $PropagationFlag, $objType) 
$objACL = Get-Acl $pathIFS 
$objACL.RemoveAccessRuleAll($objACE) 
Set-Acl $pathIFS $objACL

$objUser = New-Object System.Security.Principal.SecurityIdentifier("S-1-5-21-3232868440-3454693121-3805172430-512") 
$objACE = New-Object System.Security.AccessControl.FileSystemAccessRule($objUser, $colRights, $InheritanceFlag, $PropagationFlag, $objType) 
$objACL = Get-Acl $pathIFS 
$objACL.RemoveAccessRuleAll($objACE) 
Set-Acl $pathIFS $objACL

$ACL = (get-item $pathIFS).GetAccessControl('Access')
$acl.SetAccessRuleProtection($true, $true)
$ACL.SetAuditRuleProtection($false, $false)
$ACL.SetAuditRule($AccessRule)
$ACL | Set-Acl $pathIFS
$ACL = Get-Acl $pathIFS -Audit
$ACL.RemoveAuditRule($AccessRule)
$ACL | Set-Acl -Path $pathIFS

#добавление квоты
$fsrmName="E:\Shares\Otdel\"+$Name
$templateGB=$GB+" GB Limit"
New-FsrmQuota -Path $fsrmName -Template $templateGB -CimSession vm-ifs05

#DFS
$pathDFS="\\stc.local\otdel\"+$Name
$targetPathDFS="\\vm-ifs05\Shares\Otdel\"+$Name
$cimSession2 = New-CimSession -ComputerName "dc04"
New-DfsnFolder -Path $pathDFS -TargetPath $targetPathDFS -TimeToLiveSec 1800 -CimSession $cimSession2

"Папка создана"
Get-ChildItem  -Path \\vm-ifs05\Shares\Otdel\ -Filter 'test5' 
"fsrm template"
Get-FSRMQuota -Path $fsrmName -CimSession vm-ifs05 |select Template
"dfs"
Get-DfsnFolder  -Path $pathDFS -CimSession $cimSession2
"права доступа"
Get-Acl  $targetPathDFS |  Format-List 
"Добавить в HD: "
$pathDFS
