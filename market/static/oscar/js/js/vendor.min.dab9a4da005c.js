<?xml version='1.0' encoding='utf-8'?>
<widget id="com.herokuapp.nasara" version="0.0.1" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <preference name="loglevel" value="DEBUG" />
    <preference name="KeepRunning" value="True"/>
    <preference name="LoadUrlTimeoutValue" value="50000"/>
    <preference name="InAppBrowserStorageEnabled" value="true"/>
    <preference name="LoadingDialog" value="My Title,My Message"/>
    <preference name="ErrorUrl" value="myErrorPage.html"/>
    <preference name="ShowTitle" value="true"/>
    <preference name="LogLevel" value="VERBOSE"/>
    <preference name="AndroidLaunchMode" value="singleTop"/>
    <preference name="DefaultVolumeStream" value="call" />
    <preference name="OverrideUserAgent" value="Mozilla/5.0 My Browser" />
    <preference name="AppendUserAgent" value="My Browser" />
    <preference name="DisallowOverscroll" value="true"/>
    <preference name="Fullscreen" value="false" />
     <preference name="HideKeyboardFormAccessoryBar" value="true"/>
    <preference
        name="SplashScreen"
        value="screen" />
    <preference
        name="AutoHideSplashScreen"
        value="true" />
    <preference
        name="SplashScreenDelay"
        value="10000" />
    <feature name="Whitelist">
        <param name="android-package" value="org.apache.cordova.whitelist.WhitelistPlugin" />
        <param name="onload" value="true" />
    </feature>
    <feature name="NetworkStatus">
        <param name="android-package" value="org.apache.cordova.networkinformation.NetworkManager" />
        <param name="onload" value="true" />
    </feature>
    <feature name="HostedWebApp">
        <param name="android-package" value="com.manifoldjs.hostedwebapp.HostedWebApp" />
        <param name="onload" value="true" />
    </feature>
    <feature name="SplashScreen">
        <param name="android-package" value="org.apache.cordova.splashscreen.SplashScreen" />
        <param name="onload" value="true" />
    </feature>
    <feature name="NetworkStatus">
        <param name="android-package" value="org.apache.cordova.networkinformation.NetworkManager" />
    </feature>
    <allow-intent href="market:*" />
    <name>Nasarah</name>
    <description>
        A sample Apache Cordova application that responds to the deviceready event.
    </description>
    <author email="dev@cordova.apache.org" href="http://cordova.io">
        Apache Cordova Team
    </author>
    <content src="https://nasara.herokuapp.com/" />
    <access origin="*" />
    <allow-intent href="tel:*" />
    <allow-intent href="sms:*" />
    <allow-intent href="mailto:*" />
    <allow-intent href="geo:*" />
     <allow-navigation hap-rule="yes" href="https://nasara.herokuapp.com/*" />
    <platform>
        <splash
            density="land-hdpi"
            src="res/drawable-land-hdpi/screen.png" />
        <splash
            density="land-ldpi"
            src="res/drawable-land-ldpi/screen.png" />
        <splash
            density="land-mdpi"
            src="res/drawable-land-mdpi/screen.png" />
        <splash
            density="land-xhdpi"
            src="res/drawable-land-xhdpi/screen.png" />
        <splash
            density="port-hdpi"
            src="res/drawable-hdpi/screen.png" />
        <splash
            density="port-ldpi"
            src="res/drawable-ldpi/screen.png" />
        <splash
            density="port-mdpi"
            src="res/drawable-mdpi/screen.png" />
        <splash
            density="port-xhdpi"
            src="res/drawable-xhdpi/screen.png" />
    </platform>
</widget>