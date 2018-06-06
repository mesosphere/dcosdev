template = """
group 'com.mesosphere.sdk'
version '1.1-SNAPSHOT'

apply plugin: 'java'
apply plugin: 'application'

repositories {
    jcenter()
    mavenCentral()
    maven {
        url "http://downloads.mesosphere.com/maven/"
    }
    maven {
        url "http://downloads.mesosphere.com/maven-snapshot/"
    }
}

ext {
    junitVer = "4.12"
    systemRulesVer = "1.16.0"
    mockitoVer = "1.9.5"
}

dependencies {
    compile "mesosphere:scheduler:%(version)s"
    testCompile "mesosphere:testing:%(version)s"
}

distributions {
    main {
        baseName = 'operator-scheduler'
        version = ''
    }
}

mainClassName = 'com.mesosphere.sdk.operator.scheduler.Main'
"""
