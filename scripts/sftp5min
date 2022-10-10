param (
    $remotePath = "/",
    $wildcard = "*"
     )

$PSEmailServer = 'mail.rossiya-airlines.com'
$syslog = "C:\log\sftp5min.log"
$encoding = [System.Text.Encoding]::UTF8

$To = @('v.karpov@rossiya-airlines.com')
$Body = " "
$syslogPath="C:\log\"
If (!(test-path $syslogPath)) {
	New-Item -ItemType Directory -Force -Path $syslogPath
}

try {
	Clear-Content -path $syslog -erroraction stop
}
catch [System.Management.Automation.ItemNotFoundException] {
	add-content -path $syslog -Value ("file create")
}

try
{
    # Load WinSCP .NET assembly
    Add-Type -Path "WinSCPnet.dll"

    #Add-type -assemblyName "System.ServiceProcess"   

    # Setup session options
    $sessionOptions = New-Object WinSCP.SessionOptions -Property @{
        Protocol = [WinSCP.Protocol]::Sftp
        HostName = "sftp02.rossiya-airlines.com"
       #cred
        UserName = ""
        Password = ""
        SshHostKeyFingerprint = "ssh-rsa 4096 iQ14cUuEoeKYMk28NJrr/5mhBay6ZpcgUFR2dGwEIAs="
        PortNumber = 2222
    }
   
    $session = New-Object WinSCP.Session

    try
    {
        # Connect
        $session.Open($sessionOptions)


        # Get list of matching files in the directory
        $files =
            $session.EnumerateRemoteFiles(
                $remotePath, $wildcard, [WinSCP.EnumerationOptions]::None)

        # Any file matched?
        if ($files.Count -gt 0)
        {
        $earlier = (Get-Date).AddMinutes(-2)
        add-content -path $syslog -Value ("check")

            foreach ($fileInfo in $files)
            {
           
            if($fileInfo.LastWriteTime -lt $earlier){
            	
                    $temp1=("$($fileInfo.Name)" +                  
                    " $($fileInfo.LastWriteTime)")
                                    Write-Host ("$($fileInfo.Name)" +                  
                    " $($fileInfo.LastWriteTime)")
                    add-content -path $syslog -value ( $temp1)
                    $body=$body+$temp1+ "`n"| Out-String
                    
                    }
                                      
            }
        }
        else
        {
        	add-content -path $syslog -value ("No files matching $wildcard found")
            Write-Host "No files matching $wildcard found"
        }
        Send-MailMessage -From '' -to $To  -Body $Body -Subject "vm-sftp02" -Encoding $encoding 
    }
    catch [Exception] {
	add-content -path $syslog -value ($_.Exception.Message)
	$err = $_.Exception.Message
	Send-MailMessage -From '' -to $To  -Body $err -Subject "vm-sftp02" -Encoding $encoding 
    }
    finally
    {
        # Disconnect, clean up
        $session.Dispose()
    }

    
}
catch [Exception] {
	add-content -path $syslog -value ($_.Exception.Message)
	$err = $_.Exception.Message
	Send-MailMessage -From 'gse@rossiya-airlines.com' -to $To  -Body $err -Subject "vm-sftp02" -Encoding $encoding 
}
