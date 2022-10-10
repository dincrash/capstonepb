#TN =	S.Brovtseva
#adr LEDFPFV
#all 	Бровцева Светлана Александровна
# подаем параметр S.Brovtseva LEDFPFV Бровцева Светлана Александровна
# c:/tmp/pass пароль

param (
	[string]$TN,[string]$adr,[string]$lname,[string]$fname,[string]$oname
)
if (-not (Get-Module ActiveDirectory))
    {
		import-module ActiveDirectory
        Add-PSSnapin microsoft.e*
		
	}
$log = "C:\Scripts\Create-Mailbox.log"

$PWD = -join ((65..90) + (97..122) | Get-Random -Count 8 | % {[char]$_})
$TN| out-file -filepath C:\tmp\pass.txt -append
$PWD | out-file -filepath C:\tmp\pass.txt -append


$name=$lname+' '+$fname+' '+$oname

$fullName=$adr+' '+$name
$path="OU=Sitatex_Users,DC=sitatex,DC=local"
function Translit ([string]$inString)
{
    $Translit = @{    #Создаём хеш-таблицу соответствия символов
    [char]'а' = "a"
    [char]'А' = "A"
    [char]'б' = "b"
    [char]'Б' = "B"
    [char]'в' = "v"
    [char]'В' = "V"
    [char]'г' = "g"
    [char]'Г' = "G"
    [char]'д' = "d"
    [char]'Д' = "D"
    [char]'е' = "e"
    [char]'Е' = "E"
    [char]'ё' = "e"
    [char]'Ё' = "E"
    [char]'ж' = "zh"
    [char]'Ж' = "Zh"
    [char]'з' = "z"
    [char]'З' = "Z"
    [char]'и' = "i"
    [char]'И' = "I"
    [char]'й' = "i"
    [char]'Й' = "I"
    [char]'к' = "k"
    [char]'К' = "K"
    [char]'л' = "l"
    [char]'Л' = "L"
    [char]'м' = "m"
    [char]'М' = "M"
    [char]'н' = "n"
    [char]'Н' = "N"
    [char]'о' = "o"
    [char]'О' = "O"
    [char]'п' = "p"
    [char]'П' = "P"
    [char]'р' = "r"
    [char]'Р' = "R"
    [char]'с' = "s"
    [char]'С' = "S"
    [char]'т' = "t"
    [char]'Т' = "T"
    [char]'у' = "u"
    [char]'У' = "U"
    [char]'ф' = "f"
    [char]'Ф' = "F"
    [char]'х' = "kh"
    [char]'Х' = "Kh"
    [char]'ц' = "ts"
    [char]'Ц' = "Ts"
    [char]'ч' = "ch"
    [char]'Ч' = "Ch"
    [char]'ш' = "sh"
    [char]'Ш' = "Sh"
    [char]'щ' = "shch"
    [char]'Щ' = "Shch"
    [char]'ъ' = ""
    [char]'Ъ' = ""
    [char]'ы' = "y"
    [char]'Ы' = "Y"
    [char]'ь' = ""
    [char]'Ь' = ""
    [char]'э' = "e"
    [char]'Э' = "E"
    [char]'ю' = "iu"
    [char]'Ю' = "Iu"
    [char]'я' = "ia"
    [char]'Я' = "Ia"
    }

    $TranslitText = ""
    foreach ($CHR in $inCHR = $inString.ToCharArray())
        {
        if ($Translit[$CHR] -cne $Null) 
            { $TranslitText += $Translit[$CHR] }
        else
            { $TranslitText += $CHR }
        }
    return $TranslitText
}
New-ADuser -Enable $true -SamAccountName $TN -UserPrincipalName "$TN@sitatex.local" -Name $fullName -Surname $lName -GivenName $fName  -Description $Desc -DisplayName $fullName  -Path $Path -CannotChangePassword $true -ChangePasswordAtLogon $false -PasswordNotRequired $false -PasswordNeverExpires $true -AccountPassword (ConvertTo-SecureString -AsPlainText $PWD -Force) -ErrorAction Stop

function Create-Mail ($TN) {

	get-aduser $TN -properties mail, title | ?{$_.Mail -eq $null} | %{
		$r = $(Get-MailboxDatabase -Server mail2 | Get-Random)
		write-host $r
		$objRes = New-Object PSObject -Property @{
			TN = $_.SamAccountName;
			Name = $_.Name;
			LastName = $_.GivenName;
			Surname = $_.Surname;
			tName = $null;
			tMidleName = $null;
			tLastName = $null;
			Mail = $null;
		}
		
		if ($objRes.LastName -eq ($objRes.Name).split(" ")[0]) {
			$tLastName = Translit $objRes.LastName
			$tName = (Translit $objRes.Surname).ToCharArray()[0]		
		} else {
			$tLastName = Translit $objRes.Surname
			$tName = (Translit $objRes.LastName).ToCharArray()[0]	
		}
		$objRes.tName = $tName
		$objRes.tLastName = $tLastName

		$objRes.tMidleName = (Translit ($objRes.Name).split(" ")[2]).ToCharArray()[0]
		$c = $objRes.tName+'.'+$objRes.tLastName+'@sitatex.rossiya-airlines.com'
		if ($t = get-mailbox $c -ErrorAction SilentlyContinue) { # проверяем есть ли уже почтовый ящик по формуле N.Lastname
		
			#Если ящик по формуле N.Lastname существует, то меняем формулу на N.M.Lastname и проверяем дальше
			$c = $objRes.tName+'.'+$objRes.tMidleName+'.'+$objRes.tLastName+'@sitatex.rossiya-airlines.com'
			
			 if ($t = get-mailbox $c -ErrorAction SilentlyContinue) { # проверяем есть ли уже почтовый ящик по формуле N.M.Lastname
				$c # выводим ошибку
			 } else { #Если почтового ящика по формуле N.M.Lastname нет, то формируем переменную $mail согласно ей
				$objRes.mail = $objRes.tName+'.'+$objRes.tMidleName+'.'+$objRes.tLastName
			 }
			 
		} else {# Если почтового ящика по формуле N.Lastname нет, то формируем переменную $mail согласно ей
			$objRes.mail = $objRes.tName+'.'+$objRes.tLastName
		}
		if ($objRes.mail -ne $null)
		{	
		
			enable-mailbox $objRes.TN -Alias $objRes.mail  -Database $r
			$m = $objRes.mail+'@sitatex.rossiya-airlines.com'
		} else {
			write-host error
			$msg = $objRes.mail+";"+$objRes.Name
			add-content -path $log -value ($msg)
		}	
}
}

Create-Mail $TN


$temp=$adr+'@sitatex.rossiya-airlines.com'
$temp2=Get-ADGroup -Filter {mail -eq $temp}
Add-ADGroupMember -Identity $temp2 -Members $TN
