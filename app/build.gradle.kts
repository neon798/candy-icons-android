plugins {
    id("com.android.application")
}

android {
    namespace = "com.candyicons.android"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.candyicons.android"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    aaptOptions {
        cruncherEnabled = false
    }

    dependenciesInfo {
        includeInApk = false
        includeInBundle = false
    }
}
