#
# Conditional build:
%bcond_without	cstrike		# without Counter-Strike server
%bcond_with	dmc		# without Death-Match-Classic server
%bcond_with	ricochet	# without Ricochet server
%bcond_with	tfc		# without Team-Fortress server
#
Summary:	Half-Life - Linux Dedicated Server
Summary(pl):	Dedykowany serwer gry Half-Life dla Linuksa
Name:		hlds
Version:	1.1.2.0.STEAM
Release:	0.2
License:	custom (EULA), non-distributable
Group:		Applications/Games
Source0:        http://paszczus.darpa.pl/%{name}_l_1120_full.tgz
# NoSource0-md5:	22000aea56f7565119992587ae88dd95
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_chroot_home	/home/hlds

%description
Linux Dedicated Server of Half-Life Game.

%description -l pl
Dedykowany serwer gry Half-Life pod Linuksa.

%package cstrike
Summary:	Counter-Strike - Linux Dedicated Server
Summary(pl):	Dedykowany serwer gry Counter-Strike dla Linuksa
Group:		Applications/Games
Requires:	%{name} = %{version}-%{release}

%description cstrike
Linux Dedicated Server of Counter-Strike Game based on Half-Life
server.

%description cstrike -l pl
Dedykowany serwer gry Counter-Strike pod Linuksa oparty o serwer
Half-Life.

%package dmc
Summary:	Death-Match-Classic - Linux Dedicated Server
Summary(pl):	Dedykowany serwer gry Death-Match-Classic dla Linuksa
Group:		Applications/Games
Requires:	%{name} = %{version}-%{release}

%description dmc
Linux Dedicated Server of Death-Match-Classic Game based on Half-Life
server.

%description dmc -l pl
Dedykowany serwer gry Death-Match-Classic pod Linuksa oparty o serwer
Half-Life.

%package ricochet
Summary:	Ricochet - Linux Dedicated Server
Summary(pl):	Dedykowany serwer gry Ricochet dla Linuksa
Group:		Applications/Games
Requires:	%{name} = %{version}-%{release}

%description ricochet
Linux Dedicated Server of Ricochet Game based on Half-Life server.

%description ricochet -l pl
Dedykowany serwer gry Ricochet pod Linuksa oparty o serwer Half-Life.

%package tfc
Summary:	Team-Fortress - Linux Dedicated Server
Summary(pl):	Dedykowany serwer gry Team-Fortress dla Linuksa
Group:		Applications/Games
Requires:	%{name} = %{version}-%{release}

%description tfc
Linux Dedicated Server of Team-Fortress Game based on Half-Life
server.

%description tfc -l pl
Dedykowany serwer gry Team-Fortress pod Linuksa oparty o serwer
Half-Life.

%prep
%setup -q -n hlds_l

%build
chmod u+w ./hlds_run

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_chroot_home}/{cstrike,dmc,ricochet,tfc,valve}
install -d $RPM_BUILD_ROOT%{_libdir}

install {hlds_run,hltv,hlds_amd,hlds_amd64,hlds_i486,hlds_i686,steam} $RPM_BUILD_ROOT%{_chroot_home}
install {core_i386.so,proxy_i386.so,engine_amd.so,engine_amd64.so,engine_i486.so,engine_i686.so,filesystem_stdio_i386.so,filesystem_stdio_amd64.so} $RPM_BUILD_ROOT%{_chroot_home}
install {libSteamValidateUserIDTickets_amd64.so,libSteamValidateUserIDTickets_i386.so} $RPM_BUILD_ROOT%{_libdir}

# mv is for save space on HDD

%if %{with cstrike}
mv cstrike/* $RPM_BUILD_ROOT%{_chroot_home}/cstrike
%endif

%if %{with dmc}
mv dmc/* $RPM_BUILD_ROOT%{_chroot_home}/dmc
%endif
%if %{with ricochet}
mv ricochet/* $RPM_BUILD_ROOT%{_chroot_home}/ricochet
%endif
%if %{with tfc}
mv tfc/* $RPM_BUILD_ROOT%{_chroot_home}/tfc
%endif

mv valve/* $RPM_BUILD_ROOT%{_chroot_home}/valve

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid hlds`" ]; then
	if [ "`getgid hlds`" != "36" ]; then
		echo "Error: group hlds doesn't have gid=36. Correct this before installing hlds." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 36 -r -f hlds
fi
if [ -n "`id -u hlds 2>/dev/null`" ]; then
	if [ "`id -u hlds`" != "23" ]; then
		echo "Error: user hlds doesn't have uid=23. Correct this before installing hlds." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 23 -r -d %{_chroot_home} -s /bin/bash -c "Half-Life Dedicated Server" -g hlds hlds 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	echo "Removing user & group hlds."
	/usr/sbin/userdel hlds
	/usr/sbin/groupdel hlds
fi

%files
%defattr(644,hlds,hlds,755)
%doc linuxreadme.txt
%dir %{_chroot_home}
%attr(755,hlds,hlds) %{_chroot_home}/hlds_amd
%attr(755,hlds,hlds) %{_chroot_home}/hlds_amd64
%attr(755,hlds,hlds) %{_chroot_home}/hlds_i486
%attr(755,hlds,hlds) %{_chroot_home}/hlds_i686
%attr(755,hlds,hlds) %{_chroot_home}/hlds_run
%attr(755,hlds,hlds) %{_chroot_home}/hltv
%attr(755,hlds,hlds) %{_chroot_home}/steam
%attr(755,hlds,hlds) %{_chroot_home}/*.so

%dir %{_chroot_home}/valve
%{_chroot_home}/valve/*.txt
%{_chroot_home}/valve/*.lst
%{_chroot_home}/valve/*.wad
%{_chroot_home}/valve/valve.rc
%{_chroot_home}/valve/liblist.gam
%{_chroot_home}/valve/steam.inf
#%{_chroot_home}/valve/pak0.pak
%{_chroot_home}/valve/server.cfg
#%{_chroot_home}/valve/sierra.inf
%{_chroot_home}/valve/skill.cfg
%dir %{_chroot_home}/valve/cl_dlls
%{_chroot_home}/valve/cl_dlls/client.dll
%dir %{_chroot_home}/valve/dlls
%{_chroot_home}/valve/dlls/hl_i386.so
%dir %{_chroot_home}/valve/events
%{_chroot_home}/valve/events/*.sc
%dir %{_chroot_home}/valve/maps
%{_chroot_home}/valve/maps/*.bsp
%dir %{_chroot_home}/valve/sprites
%{_chroot_home}/valve/sprites/*.spr
%{_chroot_home}/valve/sprites/*.txt
%dir %{_chroot_home}/valve/sound
%{_chroot_home}/valve/sound/sentences.txt
%dir %{_chroot_home}/valve/sound/player
%{_chroot_home}/valve/sound/player/*.wav
%dir %{_chroot_home}/valve/sound/squeek
%{_chroot_home}/valve/sound/squeek/*.wav
%dir %{_chroot_home}/valve/sound/turret
%{_chroot_home}/valve/sound/turret/*.wav

%{_libdir}/*.so

%if %{with cstrike}
%files cstrike
%defattr(644,hlds,hlds,755)
%dir %{_chroot_home}/cstrike
%{_chroot_home}/cstrike/*.wad
%{_chroot_home}/cstrike/*.txt
#%{_chroot_home}/cstrike/cs_cbble.rad
#%{_chroot_home}/cstrike/cstrike.ico
%{_chroot_home}/cstrike/liblist.gam
%{_chroot_home}/cstrike/delta.lst
%{_chroot_home}/cstrike/server.cfg
#%dir %{_chroot_home}/cstrike/classes
#%{_chroot_home}/cstrike/classes/*.txt
%dir %{_chroot_home}/cstrike/cl_dlls
%{_chroot_home}/cstrike/cl_dlls/client.dll
%dir %{_chroot_home}/cstrike/dlls
%{_chroot_home}/cstrike/dlls/cs_i386.so
%dir %{_chroot_home}/cstrike/events
%{_chroot_home}/cstrike/events/*.sc
%dir %{_chroot_home}/cstrike/maps
#%{_chroot_home}/cstrike/maps/*.txt
%{_chroot_home}/cstrike/maps/*.bsp
#%{_chroot_home}/cstrike/maps/de_storm.res
#%dir %{_chroot_home}/cstrike/media
#%{_chroot_home}/cstrike/media/*.wav
%dir %{_chroot_home}/cstrike/models
%{_chroot_home}/cstrike/models/*.mdl
%dir %{_chroot_home}/cstrike/models/player
%dir %{_chroot_home}/cstrike/models/player/arctic
%{_chroot_home}/cstrike/models/player/arctic/arctic.mdl
%dir %{_chroot_home}/cstrike/models/player/gign
%{_chroot_home}/cstrike/models/player/gign/gign.mdl
%dir %{_chroot_home}/cstrike/models/player/gsg9
%{_chroot_home}/cstrike/models/player/gsg9/gsg9.mdl
%dir %{_chroot_home}/cstrike/models/player/guerilla
%{_chroot_home}/cstrike/models/player/guerilla/guerilla.mdl
%dir %{_chroot_home}/cstrike/models/player/leet
%{_chroot_home}/cstrike/models/player/leet/leet.mdl
%dir %{_chroot_home}/cstrike/models/player/sas
%{_chroot_home}/cstrike/models/player/sas/sas.mdl
%dir %{_chroot_home}/cstrike/models/player/terror
%{_chroot_home}/cstrike/models/player/terror/terror.mdl
%dir %{_chroot_home}/cstrike/models/player/urban
%{_chroot_home}/cstrike/models/player/urban/urban.mdl
%dir %{_chroot_home}/cstrike/models/player/vip
%{_chroot_home}/cstrike/models/player/vip/vip.mdl
%dir %{_chroot_home}/cstrike/sound
%{_chroot_home}/cstrike/sound/*.txt
%dir %{_chroot_home}/cstrike/sound/ambience
%{_chroot_home}/cstrike/sound/ambience/*.wav
%dir %{_chroot_home}/cstrike/sound/de_torn
%{_chroot_home}/cstrike/sound/de_torn/*.wav
%dir %{_chroot_home}/cstrike/sound/hostage
%{_chroot_home}/cstrike/sound/hostage/*.wav
%dir %{_chroot_home}/cstrike/sound/items
%{_chroot_home}/cstrike/sound/items/*.wav
%dir %{_chroot_home}/cstrike/sound/misc
%{_chroot_home}/cstrike/sound/misc/*.wav
%dir %{_chroot_home}/cstrike/sound/plats
%{_chroot_home}/cstrike/sound/plats/*.wav
%dir %{_chroot_home}/cstrike/sound/player
%{_chroot_home}/cstrike/sound/player/*.wav
%dir %{_chroot_home}/cstrike/sound/radio
%{_chroot_home}/cstrike/sound/radio/*.wav
%dir %{_chroot_home}/cstrike/sound/storm
%{_chroot_home}/cstrike/sound/storm/*.wav
%dir %{_chroot_home}/cstrike/sound/weapons
%{_chroot_home}/cstrike/sound/weapons/*.wav
%dir %{_chroot_home}/cstrike/sprites
%{_chroot_home}/cstrike/sprites/*.spr
#%{_chroot_home}/cstrike/sprites/*.txt
%endif

%if %{with dmc}
%files dmc
%defattr(644,hlds,hlds,755)
%dir %{_chroot_home}/dmc
%{_chroot_home}/dmc/*.txt
%{_chroot_home}/dmc/server.cfg
%{_chroot_home}/dmc/steam.inf
%{_chroot_home}/dmc/dmc.wad
%{_chroot_home}/dmc/liblist.gam
%{_chroot_home}/dmc/delta.lst
%dir %{_chroot_home}/dmc/cl_dlls
%{_chroot_home}/dmc/cl_dlls/client.dll
%dir %{_chroot_home}/dmc/dlls
%{_chroot_home}/dmc/dlls/dmc_i386.so
%{_chroot_home}/dmc/dlls/dmc.dll
%dir %{_chroot_home}/dmc/events
%{_chroot_home}/dmc/events/*.sc
%dir %{_chroot_home}/dmc/events/door
%{_chroot_home}/dmc/events/door/*.sc
%dir %{_chroot_home}/dmc/maps
%{_chroot_home}/dmc/maps/*.bsp
%dir %{_chroot_home}/dmc/models
%{_chroot_home}/dmc/models/*.mdl
%dir %{_chroot_home}/dmc/sound
%dir %{_chroot_home}/dmc/sound/ambience
%{_chroot_home}/dmc/sound/ambience/*.wav
%dir %{_chroot_home}/dmc/sound/items
%{_chroot_home}/dmc/sound/items/*.wav
%dir %{_chroot_home}/dmc/sound/misc
%{_chroot_home}/dmc/sound/misc/*.wav
%dir %{_chroot_home}/dmc/sound/player
%{_chroot_home}/dmc/sound/player/*.wav
%dir %{_chroot_home}/dmc/sound/weapons
%{_chroot_home}/dmc/sound/weapons/*.wav
%dir %{_chroot_home}/dmc/resource/
%{_chroot_home}/dmc/resource/*.tga
%dir %{_chroot_home}/dmc/sprites
%{_chroot_home}/dmc/sprites/*.spr
%{_chroot_home}/dmc/sprites/*.txt
%{_chroot_home}/dmc/sprites/logo.qc
%{_chroot_home}/dmc/sprites/flash1.tga
%endif

%if %{with ricochet}
%files ricochet
%defattr(644,hlds,hlds,755)
%dir %{_chroot_home}/ricochet
%{_chroot_home}/ricochet/*.txt
%{_chroot_home}/ricochet/delta.lst
%{_chroot_home}/ricochet/liblist.gam
%{_chroot_home}/ricochet/ricochet.wad
%dir %{_chroot_home}/ricochet/cl_dlls
%{_chroot_home}/ricochet/cl_dlls/client.dll
%dir %{_chroot_home}/ricochet/dlls
%{_chroot_home}/ricochet/dlls/ricochet_i386.so
%dir %{_chroot_home}/ricochet/events
%{_chroot_home}/ricochet/events/*.sc
%dir %{_chroot_home}/ricochet/maps
%{_chroot_home}/ricochet/maps/*.bsp
%dir %{_chroot_home}/ricochet/models
%{_chroot_home}/ricochet/models/*.mdl
%dir %{_chroot_home}/ricochet/models
%dir %{_chroot_home}/ricochet/models/player
%dir %{_chroot_home}/ricochet/models/player/female
%{_chroot_home}/ricochet/models/player/female/female.mdl
%{_chroot_home}/ricochet/models/player/female/female.bmp
%dir %{_chroot_home}/ricochet/models/player/male
%{_chroot_home}/ricochet/models/player/male/*.mdl
%dir %{_chroot_home}/ricochet/sound
%{_chroot_home}/ricochet/sound/*.wav
%dir %{_chroot_home}/ricochet/sound/Items
%{_chroot_home}/ricochet/sound/Items/gunpickup2.wav
%dir %{_chroot_home}/ricochet/sound/Vox
%{_chroot_home}/ricochet/sound/Vox/*.wav
%{_chroot_home}/ricochet/sound/Vox/*.WAV
%dir %{_chroot_home}/ricochet/sound/Weapons
%{_chroot_home}/ricochet/sound/Weapons/*.wav
%dir %{_chroot_home}/ricochet/sprites
%{_chroot_home}/ricochet/sprites/*.spr
%{_chroot_home}/ricochet/sprites/*.txt
%endif

%if %{with tfc}
%files tfc
%defattr(644,hlds,hlds,755)
%dir %{_chroot_home}/tfc
%{_chroot_home}/tfc/*.txt
%{_chroot_home}/tfc/delta.lst
%{_chroot_home}/tfc/liblist.gam
%{_chroot_home}/tfc/server.cfg
%{_chroot_home}/tfc/*.wad
%{_chroot_home}/tfc/pak0.pak
%{_chroot_home}/tfc/valve.rc
%dir %{_chroot_home}/tfc/cl_dlls
%{_chroot_home}/tfc/cl_dlls/client.dll
%dir %{_chroot_home}/tfc/dlls
%{_chroot_home}/tfc/dlls/tfc_i386.so
%dir %{_chroot_home}/tfc/events
%dir %{_chroot_home}/tfc/events/door
%{_chroot_home}/tfc/events/door/*.sc
%dir %{_chroot_home}/tfc/events/explore
%{_chroot_home}/tfc/events/explode/*.sc
%dir %{_chroot_home}/tfc/events/misc
%{_chroot_home}/tfc/events/misc/*.sc
%dir %{_chroot_home}/tfc/events/wpn
%{_chroot_home}/tfc/events/wpn/*.sc
%dir %{_chroot_home}/tfc/maps
%{_chroot_home}/tfc/maps/*.bsp
%{_chroot_home}/tfc/maps/*.txt
%dir %{_chroot_home}/tfc/models
%{_chroot_home}/tfc/models/*.mdl
%dir %{_chroot_home}/tfc/models/player
%dir %{_chroot_home}/tfc/models/player/civilian
%{_chroot_home}/tfc/models/player/civilian/civilian.mdl
%dir %{_chroot_home}/tfc/models/player/demo
%{_chroot_home}/tfc/models/player/demo/*.mdl
%dir %{_chroot_home}/tfc/models/player/engineer
%{_chroot_home}/tfc/models/player/engineer/*.mdl
%dir %{_chroot_home}/tfc/models/player/hvyweapon
%{_chroot_home}/tfc/models/player/hvyweapon/*.mdl
%dir %{_chroot_home}/tfc/models/player/medic
%{_chroot_home}/tfc/models/player/medic/*.mdl
%dir %{_chroot_home}/tfc/models/player/pyro
%{_chroot_home}/tfc/models/player/pyro/*.mdl
%dir %{_chroot_home}/tfc/models/player/scout
%{_chroot_home}/tfc/models/player/scout/*.mdl
%dir %{_chroot_home}/tfc/models/player/sniper
%{_chroot_home}/tfc/models/player/sniper/*.mdl
%dir %{_chroot_home}/tfc/models/player/soldier
%{_chroot_home}/tfc/models/player/soldier/*.mdl
%dir %{_chroot_home}/tfc/models/player/spy
%{_chroot_home}/tfc/models/player/spy/*.mdl
%dir %{_chroot_home}/tfc/sound
%dir %{_chroot_home}/tfc/sound/misc
%{_chroot_home}/tfc/sound/misc/endgame.wav
%dir %{_chroot_home}/tfc/sound/vox
%{_chroot_home}/tfc/sound/vox/*.wav
%dir %{_chroot_home}/tfc/sound/weapons
%{_chroot_home}/tfc/sound/weapons/*.wav
%dir %{_chroot_home}/tfc/tfstats
%{_chroot_home}/tfc/tfstats/*.rul
%{_chroot_home}/tfc/tfstats/*.txt
%{_chroot_home}/tfc/tfstats/tfstats_l
%endif
