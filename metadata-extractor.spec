# This spec is based on Toni Graffy's from OpenSUSE and
# Alberto Altieri's from MIB work

Name:		metadata-extractor
Summary:	A project to extract Exif and Iptc image meta-data from media files
URL:		https://www.drewnoakes.com/code/exif/
Group:		Graphics
Version:	2.3.1
Release:	3
License:	ASL 2.0
Source0:	http://www.drewnoakes.com/code/exif/%{name}-%{version}-src.jar
Patch0:		metadata-extractor-build.xml.diff
Patch1:		metadata-extractor-2.3.1-nosun.diff
Patch2:		metadata-extractor-2.3.1-unmappable.patch
BuildRequires:	ant
BuildRequires:	ant-junit
BuildRequires:	java-devel-openjdk
BuildRequires:	junit
BuildRequires:	update-alternatives
BuildRequires:	xerces-j2
BuildRequires:	xml-commons-apis
BuildRequires:	java-rpmbuild
Requires:	java >= 1.5
Requires:	jpackage-utils
BuildArch:	noarch

%description
A project to extract Exif and Iptc image meta-data from media
such as JPEG files.

What began as a simple utility to extract the date-taken from a
digital still camera (DSC) Jpeg file is now a general metadata
extraction framework. Support currently exists for Exif and Iptc
metadata segments. Extraction of these segments is provided for
Jpeg files. It is hoped that individuals with specific needs
will extend the framework by adding their own classes.

Information extracted by this library might be of use to you if
you're writing an image browser, image categoriser, photo album,
etc... I started coding this library for use in my own photo
gallery.

This metadata library is available with Java source code for usage
in the public domain.

%package javadoc
Summary:	User documentation for metadata-extractor
Group:		Development/Java
Requires:	jpackage-utils

%description javadoc
User documentation for metadata-extractor.

%prep
%setup -q -T -c
jar xf %{SOURCE0}
%patch0 -p0
%patch1 -p1
%patch2 -p1

%__rm -rf Libraries

%build
export LANG=de_DE
%ant dist-binaries javadoc

%install
%__rm -rf %{buildroot}
export NO_BRP_CHECK_BYTECODE_VERSION=true

# jars
%__install -dm 755 %{buildroot}%{_javadir}
%__install -m 644 Releases/%{name}-%{version}.jar \
	%{buildroot}%{_javadir}
pushd %{buildroot}%{_javadir}
	for jar in *-%{version}*; do
		ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
	done
popd

# javadoc
%__install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* \
	%{buildroot}%{_javadocdir}/%{name}-%{version}
%__ln_s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%clean
%__rm -rf %{buildroot}

%post javadoc
%__rm -f %{_javadocdir}/%{name}
%__ln_s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(-,root,root)
%doc ChangeLog.txt
%{_javadir}/*.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}



%changelog
* Mon Feb 20 2012 Andrey Bondrov <abondrov@mandriva.org> 2.3.1-1mdv2012.0
+ Revision: 778247
- Add patch2 to fix unmappable character for encoding ASCII error
- Add BuildRequires java-rpmbuild
- imported package metadata-extractor

