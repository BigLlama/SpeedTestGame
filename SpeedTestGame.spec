# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['SpeedTestGame.py'],
             pathex=['C:\\Users\\Ruan\\PycharmProjects\\Speedy_Typer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


a.datas += [('LT Energy Bold.ttf','C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\LT Energy Bold.ttf', "DATA"),
            ('bg.jpg', 'C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\bg.jpg', "DATA"),
            ('desk_icon.ico', 'C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\desk_icon.ico', "DATA"),
            ('icon.png', 'C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\icon.png', "DATA"),
            ('mute.png', 'C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\mute.png', "DATA"),
            ('unmute.png', 'C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\unmute.png', "DATA"),
            ('bg_music.wav', 'C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\bg_music.wav', "DATA")]


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)


exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SpeedTestGame',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='C:\\Users\\Ruan\\PycharmProjects\\SpeedTestGame\\desk_icon.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)
