$hostname = hostname
$ARS_NAME = switch ($hostname.substring(0, 3))
{
	"server-1" { "ars.server-1.job.com" }
	"server-2" { "ars.server-2.job" }
}

$success = 0
$fail = 0

# Replace the group in quotes that you want to add to
$group = "CN=**Alerts - RE Product,OU=Distribution Lists,OU=ICE Groups,DC=Job,DC=com"
# The .txt file should be 1 entity per line, the same entity type
$members = Get-Content C:\Users\nate\Documents\dl.txt.txt

foreach ($member in $members)
{
    # Replace first -parameter with whatever your base is:
    # Example: -SamAccountName ; -Email ; -Name
    # Note that Get-QADUSer will look at deactivated accounts too, hence the -Enabled flag

    # FOR ADDING USERS UNCOMMENT THE BELOW
    #$member_real = Get-QADUser -Email $member -Enabled | Select-Object -ExpandProperty DN

    # FOR ADDING GROUPS UNCOMMENT THE BELOW
    $member_real = Get-QADGroup -GroupName $member | Select-Object -ExpandProperty DN
    # $member_real = Get-ADGroup -Filter {mail -eq $member} | Select-Object -ExpandProperty DistinguishedName

    if ($member_real -ne $null)
    {
        Add-QADGroupMember -Identity "$group" -Member "$member_real" -Proxy -Service $ARS_NAME
        $success++
    }
    else
    {
        # Make sure you create a proper output folder to match this
        $member | Out-File -FilePath .\PS_Output\Confluence_NotAdded.csv -Append
        $fail++
    }
}
"$success additions made`n$fail failed"
"`nfin"
