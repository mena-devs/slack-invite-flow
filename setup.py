import setuptools

setuptools.setup(
    name="slack-invite-flow",
    version="0.1.0",
    url="https://github.com/mena-devs/slack-invite-flow",

    author="Mena Devs",
    author_email="admin@mena-devs.com",

    description="Automates Mena Devs admin tasks",
    long_description=open('README.md').read(),

    install_requires=[
        'Jinja2==2.8',
        'slackclient==1.0.2',
        'PyYaml==3.12',
    ],

    packages=['slack_invite_flow'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'slack-invite-flow = slack_invite_flow.main:main',
        ]
    }

)
