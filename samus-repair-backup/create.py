import os,io

workspace = os.path.split(os.path.realpath(__file__))[0]

headphonesFile = io.open(os.path.join(os.path.expanduser('~'),'.local/share/applications/headphones.desktop'), 'w', encoding='utf-8')
headphonesFile.write('[Desktop Entry]\n')
headphonesFile.write('Name=Headphones\n')
headphonesFile.write('Comment=enable headphones script\n')
headphonesFile.write('Exec={0}\n'.format(os.path.join(workspace, 'setup/audio/enable-headphones.sh')))
headphonesFile.write('Icon={0}\n'.format(os.path.join(workspace, 'icon/headphones.png')))
headphonesFile.write('Type=Application')
headphonesFile.close()

speakerFile = io.open(os.path.join(os.path.expanduser('~'),'.local/share/applications/speaker.desktop'), 'w', encoding='utf-8')
speakerFile.write('[Desktop Entry]\n')
speakerFile.write('Name=Speaker\n')
speakerFile.write('Comment=enable speaker script\n')
speakerFile.write('Exec={0}\n'.format(os.path.join(workspace, 'setup/audio/enable-speakers.sh')))
speakerFile.write('Icon={0}\n'.format(os.path.join(workspace, 'icon/speaker.png')))
speakerFile.write('Type=Application')
speakerFile.close()