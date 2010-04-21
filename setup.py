from setuptools import setup, find_packages

version = '1.1'

setup(name='collective.setdefaulteditor',
      version=version,
      description="Set the default editor in Plone for all existing members.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Maurits van Rees',
      author_email='m.van.rees@zestsoftware.nl',
      url='http://svn.plone.org/svn/collective/collective.setdefaulteditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
