KNOWN_MALWARE_HASHES = {
    "md5": {
        "44d88612fea8a8f36de82e1278abb02f": "EICAR-Test",
        "275a021bbfb6480f2ed6b371f5a3ebfa": "Fake-WannaCry",
        "d41d8cd98f00b204e9800998ecf8427e": "Empty File",
        "e99a18c428cb38d5f260853678922e03": "Test - abc123"
    },
    "sha256": {
        "275a021bbfb6480f2ed6b371f5a3ebfae473d3f91aa927ee9e06a12620a0c48d": "Fake-WannaCry SHA256",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Empty File SHA256"
    }
}

# Dangerous keywords in scripts (very basic detection)
DANGEROUS_KEYWORDS = [
    # Code execution and dynamic evaluation
    "eval(", "exec(", "compile(", "execfile(", "runpy.run_", "input(", "exec(", "eval(compile(", "ast.literal_eval(", "code.InteractiveConsole(", "code.InteractiveInterpreter(",
    # Module imports and dynamic loading
    "__import__", "importlib.", "imp.load_", "marshal.loads(", "pickle.loads(", "cPickle.loads(", "dill.loads(", "cloudpickle.loads(", "zipimport.zipimporter(", "pkgutil.get_data(", "pkg_resources.resource_stream(",
    # File and OS operations
    "open(", "os.system(", "os.popen(", "os.spawn", "os.fork(", "os.exec", "os.remove(", "os.unlink(", "os.rmdir(", "os.chmod(", "os.chown(", "os.rename(", "os.replace(", "os.symlink(", "os.link(", "os.truncate(", "os.fsync(", "os.fdopen(", "os.scandir(", "os.walk(", "os.listdir(", "os.startfile(", "os.read(", "os.write(", "os.lseek(", "os.forkpty(", "os.dup(", "os.dup2(",
    # Subprocess and shell
    "subprocess.", "pty.spawn(", "pty.fork()", "pty.openpty(", "pty.forkpty(", "pty.spawn(", "shlex.split(", "shlex.quote(", "shlex.join(", "pexpect.spawn(", "pexpect.run(", "pexpect.runu(", "pexpect.spawn(", "pexpect.replwrap.",
    # Networking
    "socket.", "requests.", "urllib.", "ftplib.", "telnetlib.", "http.client.", "paramiko.", "smtplib.", "poplib.", "imaplib.", "xmlrpc.client.", "xmlrpc.server.", "ftplib.FTP(", "ftplib.FTP_TLS(", "http.server.", "SimpleXMLRPCServer.", "xmlrpc.server.", "xmlrpc.client.", "asyncio.open_connection(", "asyncio.start_server(",
    # Encoding/decoding and obfuscation
    "base64.b64decode(", "base64.b64encode(", "binascii.a2b_", "binascii.b2a_", "codecs.decode(", "codecs.encode(", "rot13", "hexlify(", "unhexlify(", "zlib.decompress(", "bz2.decompress(", "lzma.decompress(", "mmap.mmap(", "marshal.loads(", "marshal.dumps(",
    # Dangerous builtins
    "globals(", "locals(", "vars(", "getattr(", "setattr(", "delattr(", "super(", "memoryview(", "eval(", "exec(", "compile(", "input(", "property(", "classmethod(", "staticmethod(",
    # Reflection and introspection
    "inspect.", "sys.modules", "sys.exit(", "sys.argv", "sys.path", "sys.settrace(", "sys.gettrace(", "sys._getframe(", "sys.exc_info(", "traceback.", "types.FunctionType(", "types.MethodType(", "types.ModuleType(", "dis.dis(", "dis.show_code(",
    # Dangerous environment access
    "os.environ", "os.getenv(", "os.putenv(", "os.setenv(", "os.unsetenv(", "os.environb", "os.get_exec_path(", "os.getlogin(", "os.getuid(", "os.geteuid(", "os.getgid(", "os.getegid(", "os.setuid(", "os.setgid(", "os.seteuid(", "os.setegid(",
    # Misc
    "shutil.rmtree(", "shutil.move(", "shutil.copy(", "shutil.copytree(", "tempfile.NamedTemporaryFile(", "tempfile.mkstemp(", "tempfile.mkdtemp(", "tempfile.SpooledTemporaryFile(", "tempfile.TemporaryDirectory(",
    # Potentially malicious patterns
    "lambda ", "chr(", "ord(", "getattr(__import__", "ast.literal_eval(", "ctypes.", "cffi.", "multiprocessing.", "threading.", "concurrent.futures.", "signal.", "atexit.", "faulthandler.", "resource.", "pwd.", "grp.", "spwd.", "crypt.", "pty.", "fcntl.", "termios.", "pty.", "pty.spawn(", "pty.forkpty(", "os.execvp(", "os.execvpe(", "os.execl(", "os.execlp(", "os.execlpe(", "os.execle(",
    # Suspicious string patterns
    "b64decode", "b85decode", "a85decode", "decode('base64'", "decode('hex'", "decode('rot13'", "decode('bz2'", "decode('zlib'", "decode('lzma'",
    # Dangerous shell patterns
    "`", "$(", "|", ";", "&&", "||", ">", "<", "2>&1", "rm -rf", "wget ", "curl ", "nc ", "ncat ", "netcat ", "bash -i", "sh -i", "python -c", "perl -e", "ruby -e", "php -r", "scp ", "ssh ", "tftp ", "ftp ", "sftp ", "powershell ", "cmd.exe", "cmd /c", "cmd /k", "regsvr32 ", "mshta ", "rundll32 ", "wmic ",
    # Dangerous Jupyter/IPython patterns
    "!wget ", "!curl ", "!nc ", "!ncat ", "!netcat ", "!bash ", "!sh ", "!python ", "!perl ", "!ruby ", "!php ", "!scp ", "!ssh ", "!tftp ", "!ftp ", "!sftp ", "!powershell ", "!cmd ", "!regsvr32 ", "!mshta ", "!rundll32 ", "!wmic ",
    # Dangerous HTML/JS patterns (for web context)
    "<script>", "javascript:", "onerror=", "onload=", "onmouseover=", "onfocus=", "onmouseenter=", "onmouseleave=", "onmouseup=", "onmousedown=", "onkeydown=", "onkeyup=", "onkeypress=",
    # Suspicious unicode and encoding tricks
    "\\u202e", "\\u202d", "\\u202a", "\\u202b", "\\u202c", "\\u200e", "\\u200f", "\\u2066", "\\u2067", "\\u2068", "\\u2069", "\\u2028", "\\u2029",
    # Suspicious file extensions
    ".exe", ".dll", ".bat", ".cmd", ".vbs", ".js", ".jse", ".wsf", ".wsh", ".ps1", ".psm1", ".scr", ".pif", ".com", ".cpl", ".msc", ".msi", ".msp", ".hta", ".jar", ".pyc", ".pyo", ".so", ".dylib", ".apk", ".ipa", ".sh", ".bash",
]