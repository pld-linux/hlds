#
# Conditional build:
%bcond_without  cstrike      # without Counter-Strike server
%bcond_with  	dmc          # without Death-Match-Classic  server
%bcond_with  	ricochet     # without Ricochet server
%bcond_with  	tfc          # without Team-Fortress server


Summary:	Half-Life - Linux Dedicated Server
Summary(pl):	Dedykowany serwer gry Half-Life dla Linuksa
Name:		hlds
Version:	3.1.1.1e
Release:	0.1
License:	Unknown
Group:		Applications/Games
Source0:	http://paszczus.darpa.pl/hlds/%{name}_l_3111_full.tar.gz
# Source0-md5:	358af895896bf6cf98d7ea4ac6072fd2
Source1:	http://paszczus.darpa.pl/hlds/cs_15_full.tar.gz
# Source1-md5:	d688876fa2864ff69ff808432c9e6fe7
Source2:	http://paszczus.darpa.pl/hlds/%{name}_l_3111e_update.tar.gz
# Source2-md5:	0156a57f81b38c7a443013ef57e20257
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
BuildArch:	noarch
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
Requires:       %{name} = %{version}-%{release}

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
Requires:       %{name} = %{version}-%{release}

%description ricochet
Linux Dedicated Server of Ricochet Game based on Half-Life server.

%description ricochet -l pl
Dedykowany serwer gry Ricochet pod Linuksa oparty o serwer Half-Life.

%package tfc
Summary:	Team-Fortress - Linux Dedicated Server
Summary(pl):	Dedykowany serwer gry Team-Fortress dla Linuksa
Group:		Applications/Games
Requires:       %{name} = %{version}-%{release}

%description tfc
Linux Dedicated Server of Team-Fortress Game based on Half-Life
server.

%description tfc -l pl
Dedykowany serwer gry Team-Fortress pod Linuksa oparty o serwer
Half-Life.

%prep
%setup -q -n hlds_l

%build

%if %{with cstrike}
cp %{SOURCE1} .
tar zxf %{SOURCE1}
rm -f cs_15_full.tar.gz
%endif

cp %{SOURCE2} .
tar zxf %{SOURCE2}
cp -a hlds_update/* .
rm -f hlds_l_3111e_update.tar.gz

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_chroot_home}/{cstrike,dmc,ricochet,tfc,valve}
install -d $RPM_BUILD_ROOT%{_libdir}

install {hlds,hlds_run,hltv,hlds_amd,hlds_i486,hlds_i686} $RPM_BUILD_ROOT%{_chroot_home}/
install {hltv.cfg,engine_i386.so,kver.kp,core_i386.so,director_i386.so,proxy_i386.so,engine_amd.so,engine_i486.so,engine_i686.so,filesystem_stdio_i386.so} $RPM_BUILD_ROOT%{_chroot_home}/
install {libSteamValidateUserIDTickets.so,libSteamValidateUserIDTickets_i386.so,libhlwon.so} $RPM_BUILD_ROOT%{_libdir}

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
%doc ChangeLog EULA.txt HLTV-Readme.txt linuxreadme.txt
%dir %{_chroot_home}
%attr(755,hlds,hlds) %{_chroot_home}/hlds
%attr(755,hlds,hlds) %{_chroot_home}/hlds_amd
%attr(755,hlds,hlds) %{_chroot_home}/hlds_i486
%attr(755,hlds,hlds) %{_chroot_home}/hlds_i686
%attr(755,hlds,hlds) %{_chroot_home}/hlds_run
%attr(755,hlds,hlds) %{_chroot_home}/hltv
%attr(755,hlds,hlds) %{_chroot_home}/*.so

%dir %{_chroot_home}/valve
%{_chroot_home}/valve/*.txt
%{_chroot_home}/valve/*.lst
%{_chroot_home}/valve/*.wad
%{_chroot_home}/valve/valve.rc
%{_chroot_home}/valve/liblist.gam
%{_chroot_home}/valve/pak0.pak
%{_chroot_home}/valve/server.cfg
%{_chroot_home}/valve/sierra.inf
%{_chroot_home}/valve/skill.cfg
%{_chroot_home}/valve/cl_dlls/client.dll
%{_chroot_home}/valve/dlls/hl_i386.so
%{_chroot_home}/valve/events/*.sc
%{_chroot_home}/valve/maps/*.bsp
%{_chroot_home}/valve/sprites/*.spr

%{_chroot_home}/kver.kp
%{_chroot_home}/hltv.cfg
%{_libdir}/*.so

%if %{with cstrike}
%files cstrike
%defattr(644,hlds,hlds,755)
%dir %{_chroot_home}/cstrike
%{_chroot_home}/cstrike/*.wad
%{_chroot_home}/cstrike/*.txt
%{_chroot_home}/cstrike/cs_cbble.rad
%{_chroot_home}/cstrike/cstrike.ico
%{_chroot_home}/cstrike/liblist.gam
%{_chroot_home}/cstrike/delta.lst
%{_chroot_home}/cstrike/server.cfg
%{_chroot_home}/cstrike/classes/*.txt
%{_chroot_home}/cstrike/cl_dlls/client.dll
%{_chroot_home}/cstrike/dlls/cs_i386.so
%{_chroot_home}/cstrike/events/*.sc
%{_chroot_home}/cstrike/maps/*.txt
%{_chroot_home}/cstrike/maps/*.bsp
%{_chroot_home}/cstrike/maps/de_storm.res
%{_chroot_home}/cstrike/media/*.wav
%{_chroot_home}/cstrike/models/*.mdl
%{_chroot_home}/cstrike/models/player/arctic/arctic.mdl
%{_chroot_home}/cstrike/models/player/gign/gign.mdl
%{_chroot_home}/cstrike/models/player/gsg9/gsg9.mdl
%{_chroot_home}/cstrike/models/player/guerilla/guerilla.mdl
%{_chroot_home}/cstrike/models/player/leet/leet.mdl
%{_chroot_home}/cstrike/models/player/sas/sas.mdl
%{_chroot_home}/cstrike/models/player/terror/terror.mdl
%{_chroot_home}/cstrike/models/player/urban/urban.mdl
%{_chroot_home}/cstrike/models/player/vip/vip.mdl
%{_chroot_home}/cstrike/sound/*.txt
%{_chroot_home}/cstrike/sound/ambience/*.wav
%{_chroot_home}/cstrike/sound/de_torn/*.wav
%{_chroot_home}/cstrike/sound/hostage/*.wav
%{_chroot_home}/cstrike/sound/items/*.wav
%{_chroot_home}/cstrike/sound/misc/*.wav
%{_chroot_home}/cstrike/sound/plats/*.wav
%{_chroot_home}/cstrike/sound/player/*.wav
%{_chroot_home}/cstrike/sound/radio/*.wav
%{_chroot_home}/cstrike/sound/storm/*.wav
%{_chroot_home}/cstrike/sound/weapons/*.wav
%{_chroot_home}/cstrike/sprites/*.spr
%{_chroot_home}/cstrike/sprites/*.txt
%endif

%if %{with dmc}
%files dmc
%defattr(644,hlds,hlds,755)
%dir %{_chroot_home}/dmc
%{_chroot_home}/dmc/*.txt
%{_chroot_home}/dmc/server.cfg
%{_chroot_home}/dmc/dmc.wad
%{_chroot_home}/dmc/liblist.gam
%{_chroot_home}/dmc/delta.lst
%{_chroot_home}/dmc/cl_dlls/client.dll
%{_chroot_home}/dmc/dlls/dmc_i386.so
%{_chroot_home}/dmc/events/*.sc
%{_chroot_home}/dmc/events/door/*.sc
%{_chroot_home}/dmc/maps/*.bsp
%{_chroot_home}/dmc/models/*.mdl
%{_chroot_home}/dmc/sound/ambience/*.wav
%{_chroot_home}/dmc/sound/items/*.wav
%{_chroot_home}/dmc/sound/misc/*.wav
%{_chroot_home}/dmc/sound/player/*.wav
%{_chroot_home}/dmc/sound/weapons/*.wav
%{_chroot_home}/dmc/sprites/*.spr
%{_chroot_home}/dmc/sprites/*.txt
%{_chroot_home}/dmc/sprites/Buildspr.bat
%{_chroot_home}/dmc/sprites/flash1.tga
%{_chroot_home}/dmc/sprites/flash2.pcx
%{_chroot_home}/dmc/sprites/logo.qc
%endif

%if %{with ricochet}
%files ricochet
%defattr(644,hlds,hlds,755)
%dir %{_chroot_home}/ricochet
%{_chroot_home}/ricochet/*.txt
%{_chroot_home}/ricochet/delta.lst
%{_chroot_home}/ricochet/liblist.gam
%{_chroot_home}/ricochet/ricochet.wad
%{_chroot_home}/ricochet/cl_dlls/client.dll
%{_chroot_home}/ricochet/dlls/ricochet_i386.so
%{_chroot_home}/ricochet/events/*.sc
%{_chroot_home}/ricochet/maps/*.bsp
%{_chroot_home}/ricochet/models/*.mdl
%{_chroot_home}/ricochet/models/player/female/female.mdl
%{_chroot_home}/ricochet/models/player/female/female.bmp
%{_chroot_home}/ricochet/models/player/male/*.mdl
%{_chroot_home}/ricochet/sound/*.wav
%{_chroot_home}/ricochet/sound/Items/gunpickup2.wav
%{_chroot_home}/ricochet/sound/Vox/*.wav
%{_chroot_home}/ricochet/sound/Vox/*.WAV
%{_chroot_home}/ricochet/sound/Weapons/*.wav
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
%{_chroot_home}/tfc/cl_dlls/client.dll
%{_chroot_home}/tfc/dlls/tfc_i386.so
%{_chroot_home}/tfc/events/door/*.sc
%{_chroot_home}/tfc/events/explode/*.sc
%{_chroot_home}/tfc/events/misc/*.sc
%{_chroot_home}/tfc/events/wpn/*.sc
%{_chroot_home}/tfc/maps/*.bsp
%{_chroot_home}/tfc/maps/*.txt
%{_chroot_home}/tfc/models/*.mdl
%{_chroot_home}/tfc/models/player/civilian/civilian.mdl
%{_chroot_home}/tfc/models/player/demo/*.mdl
%{_chroot_home}/tfc/models/player/engineer/*.mdl
%{_chroot_home}/tfc/models/player/hvyweapon/*.mdl
%{_chroot_home}/tfc/models/player/medic/*.mdl
%{_chroot_home}/tfc/models/player/pyro/*.mdl
%{_chroot_home}/tfc/models/player/scout/*.mdl
%{_chroot_home}/tfc/models/player/sniper/*.mdl
%{_chroot_home}/tfc/models/player/soldier/*.mdl
%{_chroot_home}/tfc/models/player/spy/*.mdl
%{_chroot_home}/tfc/sound/misc/endgame.wav
%{_chroot_home}/tfc/sound/vox/*.wav
%{_chroot_home}/tfc/sound/weapons/*.wav
%{_chroot_home}/tfc/tfstats/*.rul
%{_chroot_home}/tfc/tfstats/*.txt
%{_chroot_home}/tfc/tfstats/tfstats_l
%endif