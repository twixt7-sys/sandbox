# Windows Server 2022 Domain Controller Lab – Step-by-Step Guide

Replace **Lastname** everywhere with your real surname (example below uses `Smith`).

---

## Part 1 – Install Windows Server 2022 in VirtualBox

1. Download the **Windows Server 2022 Evaluation ISO** from the Microsoft Evaluation Center.
2. In VirtualBox click **New**:
   - Name: `SAM-Smith`, ISO Image: the Server 2022 ISO
   - Tick **Skip Unattended Installation** (so you choose the edition yourself)
   - RAM: 4096 MB, CPUs: 2, Disk: 50 GB
3. **Start** the VM. Choose language → **Install now**.
4. Select **Windows Server 2022 Standard Evaluation (Desktop Experience)** – the *Desktop Experience* one, otherwise you get no GUI.
5. Accept the license → **Custom: Install Windows only** → select the disk → **Next**.
6. When it reboots, set the **Administrator** password (e.g. `P@ssw0rd123`). Write it down.
7. Log in (VirtualBox menu **Input → Keyboard → Insert Ctrl-Alt-Del**, or Right-Ctrl+Del).
8. Optional but helpful: **Devices → Insert Guest Additions CD image**, run `VBoxWindowsAdditions.exe`, reboot (gives proper screen resolution).

## Part 2 – Rename the server to SAM-Lastname

1. Right-click **Start → System** → **Rename this PC** → type `SAM-Smith` → **Next** → **Restart now**.

   PowerShell alternative:
   ```powershell
   Rename-Computer -NewName "SAM-Smith" -Restart
   ```
2. After reboot confirm: open PowerShell and run `hostname`.

> Tip: give the server a static IP before promoting it (Settings → Network → Ethernet → Change adapter options → IPv4 → e.g. IP `192.168.1.10`, mask `255.255.255.0`, gateway your router, **Preferred DNS `127.0.0.1`**). With VirtualBox NAT you can simply keep DHCP and accept the warning later – it still works for this lab.

## Part 3 – Install the Active Directory Domain Services role

1. **Server Manager → Manage → Add Roles and Features**.
2. **Next** → *Role-based or feature-based installation* → **Next** → select `SAM-Smith` → **Next**.
3. Tick **Active Directory Domain Services** → click **Add Features** in the pop-up → **Next**.
4. **Next** through Features and AD DS pages → **Install**. Wait until it finishes.

   PowerShell alternative:
   ```powershell
   Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
   ```

## Part 4 – Promote the server to a Domain Controller (Lastname.com)

1. In Server Manager click the **yellow flag** → **Promote this server to a domain controller**.
2. Choose **Add a new forest** → Root domain name: `Smith.com` → **Next**.
3. Leave functional levels at default; keep **DNS server** and **Global Catalog** ticked; enter a **DSRM password** → **Next**.
4. Ignore the DNS delegation warning → **Next**.
5. NetBIOS name auto-fills (`SMITH`) → **Next** → keep default paths → **Next** → **Next**.
6. Prerequisites check passes (warnings are fine) → **Install**. The server reboots automatically.
7. Log in now as **SMITH\Administrator** (same password as before).

   PowerShell alternative:
   ```powershell
   Install-ADDSForest -DomainName "Smith.com" -InstallDns
   ```

## Part 5 – Create User1

1. **Server Manager → Tools → Active Directory Users and Computers** (or run `dsa.msc`).
2. Expand **Smith.com** → right-click **Users** → **New → User**.
3. First name `User1`, User logon name `User1` → **Next**.
4. Password e.g. `P@ssw0rd123` (must be complex). **Untick** *User must change password at next logon*, tick **Password never expires** → **Next → Finish**.

### 📸 Screenshot 1 – User Account
Click the **Users** container so `User1` is visible in the right pane **and** `Smith.com` is visible in the left tree. Take the screenshot.

## Part 6 – Create Group1 and add User1

1. Right-click **Users** → **New → Group** → Name `Group1`, Scope **Global**, Type **Security** → **OK**.
2. Double-click **Group1 → Members → Add** → type `User1` → **Check Names → OK → OK**.

### 📸 Screenshot 2 – Group Account
Show `Group1` in the Users container with `Smith.com` visible in the tree.

## Part 7 – Allow User1 to log on to the server (important!)

By default normal domain users **cannot sign in locally to a Domain Controller** ("The sign-in method you're trying to use isn't allowed"). Fix it:

1. **Server Manager → Tools → Group Policy Management**.
2. Expand **Forest → Domains → Smith.com → Domain Controllers** → right-click **Default Domain Controllers Policy → Edit**.
3. Go to **Computer Configuration → Policies → Windows Settings → Security Settings → Local Policies → User Rights Assignment**.
4. Double-click **Allow log on locally** → **Add User or Group** → `Group1` → **OK → OK**.
5. Open Command Prompt as admin and run:
   ```cmd
   gpupdate /force
   ```

## Part 8 – Create MyFolder1 and set permissions

1. Open **File Explorer → This PC → Local Disk (C:)** → right-click → **New → Folder** → name it `MyFolder1`.
2. Right-click **MyFolder1 → Properties → Security** tab → **Edit… → Add…** → type `Group1` (or `User1`) → **Check Names → OK**.
3. With Group1 selected tick **Allow** for **Read** and **Write** (tick **Modify** too so the user can edit/save files) → **Apply → OK → OK**.

   PowerShell alternative:
   ```powershell
   New-Item -Path C:\MyFolder1 -ItemType Directory
   icacls C:\MyFolder1 /grant "SMITH\Group1:(OI)(CI)M"
   ```
4. (Optional – if your instructor wants a network share) **Sharing** tab → **Advanced Sharing** → tick **Share this folder** → **Permissions** → add Group1 with **Change** + **Read**.

## Part 9 – Log in as User1 and create User1File.txt

1. **Start → user icon → Sign out**.
2. At the login screen pick **Other user** → username `SMITH\User1`, password `P@ssw0rd123`.
3. Open **File Explorer → C:\MyFolder1** → right-click → **New → Text Document** → name it `User1File.txt`.
4. Open **PowerShell** and run:
   ```powershell
   whoami
   hostname
   Get-ChildItem C:\MyFolder1
   ```

### 📸 Screenshot 3 – User Access
Arrange the PowerShell window (showing `smith\user1` and the file listing) next to the File Explorer window showing `User1File.txt` in MyFolder1. Screenshot both.

## Part 10 – Log in as Administrator and verify

1. Sign out → **Other user** → `SMITH\Administrator`.
2. Open **C:\MyFolder1** in File Explorer – `User1File.txt` should be there.
3. In PowerShell run:
   ```powershell
   whoami
   Get-ChildItem C:\MyFolder1
   Get-Acl C:\MyFolder1\User1File.txt | Format-List Owner
   ```
   The owner line (`SMITH\User1`) is a nice extra proof that User1 created it.

### 📸 Screenshot 4 – Administrator Verification
PowerShell showing `smith\administrator` + the file listing, beside File Explorer showing the file.

> Taking screenshots: inside the VM use **Snipping Tool** (Win+Shift+S) and save to a file, or in VirtualBox use **View → Take Screenshot** (Host+E), which saves the PNG on your host PC.

## Part 11 – Build the submission

1. Open **Microsoft Word** → add a title, your name, and date.
2. For each screenshot add a heading/caption:
   - *Figure 1 – User Account: User1 in Smith.com*
   - *Figure 2 – Group Account: Group1 in Smith.com*
   - *Figure 3 – User Access: logged in as User1, User1File.txt in MyFolder1*
   - *Figure 4 – Administrator Verification: logged in as Administrator, User1File.txt present*
3. **Insert → Pictures** for each; resize to page width so text is readable.
4. **File → Save As → PDF** (or **Export → Create PDF/XPS**).
5. Name the file exactly using your instructor's required format (it was blank in the copy you pasted – check the original assignment, e.g. `Lastname_ActivityName.pdf`).
6. Submit through the designated channel.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "The sign-in method you're trying to use isn't allowed" for User1 | Part 7 not applied – re-check *Allow log on locally* and run `gpupdate /force` |
| "Access denied" creating the file | Group1 lacks Write/Modify on MyFolder1, or User1 isn't a member of Group1 – sign out and back in after fixing |
| Password rejected when creating User1 | Needs 7+ chars with upper, lower, digit/symbol |
| Promotion fails on DNS | Set Preferred DNS to `127.0.0.1` on the adapter and retry |
| Only a black command prompt after install | You picked the non-Desktop-Experience edition – reinstall and choose *(Desktop Experience)* |
