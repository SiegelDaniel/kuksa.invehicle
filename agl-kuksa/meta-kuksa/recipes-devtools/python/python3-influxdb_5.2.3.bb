SUMMARY = "A Python library for interacting with InfluxDB."
HOMEPAGE = "https://github.com/influxdata/influxdb-python"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=046523829184aac3703a4c60c0ae2104"

inherit pypi setuptools3

SRC_URI[md5sum] = "01db77f4ca825d554a78804a4be4a353"
SRC_URI[sha256sum] = "30276c7e04bf7659424c733b239ba2f0804d7a1f3c59ec5dd3f88c56176c8d36"

RDEPENDS_${PN} += " \
	python3-dateutil \
	python3-pytz \
	python3-requests \
	python3-six \
	python3-msgpack"

