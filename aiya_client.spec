# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src\\aiya_client.py'],
             pathex=['C:\\Users\\DHAdmin\\yqf\\code\\aiya-client\\src'],
             binaries=[],
             datas=[],
             hiddenimports=['common', 'cut_cut_cut'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [
    ("cut_cut_cut_release_notes.txt","src\\cut_cut_cut\\cut_cut_cut_release_notes.txt","DATA"),
    ("release_notes.txt","src\\release_notes.txt","DATA"),
    ("rabbitmq.yml","src\\mq\\rabbitmq.yml","DATA")
]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AiyaClient',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
