import os, shutil
BASE = os.path.abspath(".")
PROJECT = os.path.join(BASE, "android-project")
WWW_URL = "https://xiaoyang0609.github.io/desktop-pet/"

def main():
    if os.path.exists(PROJECT): shutil.rmtree(PROJECT)
    pkg_dir = "com/desktop/pet"
    for d in ["app/src/main/java/"+pkg_dir,"app/src/main/res/drawable","app/src/main/res/values",
              "app/src/main/res/mipmap-hdpi","app/src/main/res/mipmap-mdpi","app/src/main/res/mipmap-xhdpi",
              "app/src/main/res/mipmap-xxhdpi","app/src/main/res/mipmap-xxxhdpi",
              "app/src/main/res/mipmap-anydpi-v26","gradle/wrapper"]:
        os.makedirs(os.path.join(PROJECT,d), exist_ok=True)
    
    with open(os.path.join(PROJECT,"settings.gradle"),"w") as f:
        f.write("""pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = "DesktopPet"; include ':app'""")
    with open(os.path.join(PROJECT,"build.gradle"),"w") as f:
        f.write("""plugins { id 'com.android.application' version '8.2.0' apply false }""")
    with open(os.path.join(PROJECT,"gradle.properties"),"w") as f:
        f.write("org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\\nandroid.useAndroidX=true\\nandroid.enableJetifier=true")
    with open(os.path.join(PROJECT,"gradle/wrapper/gradle-wrapper.properties"),"w") as f:
        f.write("distributionBase=GRADLE_USER_HOME\\ndistributionPath=wrapper/dists\\ndistributionUrl=https\\\\://services.gradle.org/distributions/gradle-8.5-bin.zip\\nzipStoreBase=GRADLE_USER_HOME\\nzipStorePath=wrapper/dists\\n")
    with open(os.path.join(PROJECT,"app/build.gradle"),"w") as f:
        f.write("""plugins { id 'com.android.application' }
android { namespace 'com.desktop.pet'; compileSdk 34; defaultConfig { applicationId 'com.desktop.pet'; minSdk 21; targetSdk 34; versionCode 1; versionName '1.0' }
buildTypes { release { minifyEnabled false; proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro' } }
compileOptions { sourceCompatibility JavaVersion.VERSION_17; targetCompatibility JavaVersion.VERSION_17 } }
dependencies { implementation 'androidx.appcompat:appcompat:1.6.1'; implementation 'androidx.webkit:webkit:1.9.0' }""")
    with open(os.path.join(PROJECT,"app/proguard-rules.pro"),"w") as f:
        f.write("")
    with open(os.path.join(PROJECT,"app/src/main/res/values/styles.xml"),"w") as f:
        f.write("""<?xml version="1.0"?><resources><style name="AppTheme" parent="Theme.AppCompat.NoActionBar"><item name="android:windowFullscreen">true</item><item name="android:windowNoTitle">true</item><item name="android:statusBarColor">#1a1a2e</item><item name="android:navigationBarColor">#1a1a2e</item></style></resources>""")
    with open(os.path.join(PROJECT,"app/src/main/res/values/strings.xml"),"w") as f:
        f.write("""<?xml version="1.0"?><resources><string name="app_name">桌面宠物</string></resources>""")
    with open(os.path.join(PROJECT,"app/src/main/AndroidManifest.xml"),"w") as f:
        f.write("""<?xml version="1.0"?><manifest package="com.desktop.pet"><uses-permission android:name="android.permission.INTERNET"/>
<application android:label="桌面宠物" android:theme="@style/AppTheme" android:icon="@mipmap/ic_launcher" android:usesCleartextTraffic="false">
<activity android:name=".MainActivity" android:exported="true"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>""")
    with open(os.path.join(PROJECT,"app/src/main/java/"+pkg_dir+"/MainActivity.java"),"w") as f:
        f.write("""package com.desktop.pet;
import android.os.Bundle; import android.view.View; import android.webkit.*;
import android.widget.*; import androidx.appcompat.app.AppCompatActivity;
public class MainActivity extends AppCompatActivity {
    WebView wv; ProgressBar pb;
    @Override protected void onCreate(Bundle b) {
        super.onCreate(b); FrameLayout l = new FrameLayout(this); wv = new WebView(this);
        WebSettings s = wv.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
        s.setLoadWithOverviewMode(true); s.setUseWideViewPort(true); s.setBuiltInZoomControls(false);
        wv.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        wv.setWebViewClient(new WebViewClient() {
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                String u = r.getUrl().toString();
                if(u.contains("xiaoyang0609.github.io/desktop-pet")) return false;
                startActivity(new android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(u)));
                return true;
            }
            public void onPageStarted(WebView v, String u, android.graphics.Bitmap f) { pb.setVisibility(View.VISIBLE); }
            public void onPageFinished(WebView v, String u) { pb.setVisibility(View.GONE); }
        });
        wv.setWebChromeClient(new WebChromeClient() { public void onProgressChanged(WebView v, int p) { pb.setProgress(p); } });
        l.addView(wv, new FrameLayout.LayoutParams(-1, -1));
        pb = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal); pb.setMax(100); pb.setVisibility(View.GONE);
        l.addView(pb, new FrameLayout.LayoutParams(-1, (int)(3*getResources().getDisplayMetrics().density+0.5f)));
        setContentView(l); wv.loadUrl(""""+'"'+WWW_URL+'"'+""");
    }
    @Override public void onBackPressed() { if(wv.canGoBack()) wv.goBack(); else super.onBackPressed(); }
}""")
    # Icons
    try:
        from PIL import Image, ImageDraw
        for den,px in {'mdpi':48,'hdpi':72,'xhdpi':96,'xxhdpi':144,'xxxhdpi':192}.items():
            img = Image.new('RGBA',(px,px),(26,26,46,255)); draw = ImageDraw.Draw(img)
            cx,cy,r = px//2,px//2-px//8,px//3
            draw.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(74,144,217,255))
            er = px//12; draw.ellipse([cx-r//2-er,cy-er*2,cx-r//2+er,cy+er*2],fill=(255,255,255,255))
            draw.ellipse([cx+r//2-er,cy-er*2,cx+r//2+er,cy+er*2],fill=(255,255,255,255))
            nr=px//20; draw.polygon([(cx-nr,cy+er),(cx+nr,cy+er),(cx,cy+er+nr*2)],fill=(255,182,193,255))
            img.save(os.path.join(PROJECT,"app/src/main/res/mipmap-"+den+"/ic_launcher.png"),"PNG")
    except ImportError:
        for den in ['mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']:
            open(os.path.join(PROJECT,"app/src/main/res/mipmap-"+den+"/ic_launcher.png"),"wb").write(bytes([137,80,78,71,13,10,26,10,0,0,0,13,73,72,68,82,0,0,0,48,0,0,0,48,8,6,0,0,0,87,95,191,207,0,0,0,1,115,82,71,66,0,174,206,28,233,0,0,0,4,103,65,77,65,0,0,177,143,11,252,97,5,0,0,0,9,112,72,89,115,0,0,14,196,0,0,14,196,1,149,43,46,65,0,0,0,94,73,68,65,84,72,199,237,213,65,10,0,32,8,68,209,163,245,254,87,118,17,20,36,173,82,65,131,79,100,246,15,134,221,181,241,130,91,128,13,29,64,23,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,215,3,104,124,5,236,241,65,42,43,0,0,0,0,73,69,78,68,174,66,96,130]))
    print("Project created!")

if __name__ == "__main__": main()