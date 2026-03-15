from flask import Flask, request, jsonify, render_template, session
import numpy as np, urllib.parse
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
app.secret_key = "audiodna_secret_key_2025"

def yt(title, artist):
    q = urllib.parse.quote_plus(f"{title} {artist} official")
    return f"https://www.youtube.com/results?search_query={q}"

COVERS = [
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1504898770365-14faca6a7320?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1571330735066-03aaa9429d89?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1487180144351-b8472da7d491?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1446057032654-9d8885db76c6?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1455651512878-0ddbb4c4d0a5?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1483412033650-1015ddeb83d1?w=300&h=300&fit=crop",
    "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=300&h=300&fit=crop",
]

def c(i): return COVERS[i % len(COVERS)]

def s(idx,title,artist,genre,mood,country,energy,dance,valence,tempo):
    return {"id":str(idx),"title":title,"artist":artist,"genre":genre,"mood":mood,
            "country":country,"cover":c(idx),"youtube_link":yt(title,artist),
            "energy":energy,"danceability":dance,"valence":valence,"tempo":tempo}

_raw = [
    # ARIJIT SINGH (20 songs)
    ("Tum Hi Ho","Arijit Singh","Pop","Sad","India",0.30,0.40,0.20,72),
    ("Teri Mitti","Arijit Singh","Pop","Sad","India",0.35,0.42,0.22,75),
    ("Channa Mereya","Arijit Singh","Pop","Sad","India",0.32,0.42,0.18,70),
    ("Ae Dil Hai Mushkil","Arijit Singh","Pop","Sad","India",0.28,0.38,0.16,68),
    ("Kabira","Arijit Singh","Pop","Relax","India",0.40,0.45,0.55,82),
    ("Phir Le Aaya Dil","Arijit Singh","Pop","Sad","India",0.30,0.38,0.20,74),
    ("Suno Na Sangemarmar","Arijit Singh","Pop","Happy","India",0.55,0.58,0.70,90),
    ("Muskurane","Arijit Singh","Pop","Happy","India",0.50,0.55,0.72,88),
    ("Sooraj Dooba Hain","Arijit Singh","Pop","Sad","India",0.33,0.40,0.25,76),
    ("Agar Tum Saath Ho","Arijit Singh","Pop","Sad","India",0.29,0.37,0.18,70),
    ("Bulleya","Arijit Singh","Pop","Relax","India",0.42,0.48,0.60,85),
    ("Laal Ishq","Arijit Singh","Pop","Sad","India",0.31,0.39,0.22,72),
    ("Janam Janam","Arijit Singh","Pop","Happy","India",0.52,0.57,0.68,92),
    ("Ilahi","Arijit Singh","Pop","Happy","India",0.60,0.65,0.75,96),
    ("Gerua","Arijit Singh","Pop","Happy","India",0.55,0.60,0.72,94),
    ("Kun Faya Kun","Arijit Singh","Sufi","Relax","India",0.25,0.30,0.60,62),
    ("Tum Se Hi","Arijit Singh","Pop","Sad","India",0.28,0.36,0.18,68),
    ("Kesariya","Arijit Singh","Pop","Happy","India",0.60,0.65,0.72,96),
    ("Teri Baaton Mein Aisa","Arijit Singh","Pop","Happy","India",0.62,0.65,0.76,98),
    ("Apna Bana Le","Arijit Singh","Pop","Happy","India",0.58,0.62,0.74,92),
    ("Naina","Arijit Singh","Pop","Sad","India",0.32,0.38,0.22,70),
    ("O Maahi","Arijit Singh","Pop","Sad","India",0.34,0.40,0.24,72),
    ("Manwa Laage","Arijit Singh","Pop","Happy","India",0.62,0.65,0.78,98),
    ("Tu Hi Yaar Mera","Arijit Singh","Pop","Happy","India",0.60,0.65,0.76,96),
    ("Deva Deva","Arijit Singh","Pop","Focus","India",0.65,0.68,0.60,100),
    ("Jhoome Jo Pathaan","Arijit Singh","Pop","Party","India",0.82,0.85,0.82,115),
    ("Ghungroo","Arijit Singh","Pop","Party","India",0.75,0.78,0.78,108),
    ("Dilnashin Dilnashin","Arijit Singh","Pop","Sad","India",0.30,0.36,0.22,70),
    # SHREYA GHOSHAL (12 songs)
    ("Sun Raha Hai","Shreya Ghoshal","Pop","Sad","India",0.35,0.38,0.25,68),
    ("Teri Meri","Shreya Ghoshal","Pop","Sad","India",0.30,0.35,0.22,66),
    ("Barso Re","Shreya Ghoshal","Classical","Happy","India",0.55,0.60,0.75,95),
    ("Dola Re Dola","Shreya Ghoshal","Classical","Happy","India",0.62,0.65,0.78,100),
    ("Jab Tak Hai Jaan","Shreya Ghoshal","Pop","Sad","India",0.32,0.38,0.20,72),
    ("Dhoom Taana","Shreya Ghoshal","Pop","Happy","India",0.70,0.72,0.82,108),
    ("Piyu Bole","Shreya Ghoshal","Classical","Relax","India",0.40,0.45,0.60,82),
    ("Teri Ore","Shreya Ghoshal","Pop","Happy","India",0.58,0.62,0.74,95),
    ("Mann Mohana","Shreya Ghoshal","Classical","Relax","India",0.38,0.42,0.58,78),
    ("Nagada Sang Dhol","Shreya Ghoshal","Pop","Party","India",0.82,0.85,0.85,118),
    ("Ishq Wala Love","Shreya Ghoshal","Pop","Happy","India",0.60,0.65,0.78,96),
    ("Saibo","Shreya Ghoshal","Pop","Relax","India",0.40,0.45,0.60,82),
    # KUMAR SANU / UDIT NARAYAN / CLASSICS
    ("Ek Ladki Ko Dekha","Kumar Sanu","Pop","Happy","India",0.60,0.65,0.80,98),
    ("Dil Hai Ki Manta Nahin","Kumar Sanu","Pop","Happy","India",0.62,0.68,0.78,100),
    ("Mere Sapno Ki Rani","Kumar Sanu","Pop","Happy","India",0.58,0.62,0.76,96),
    ("Tujhe Dekha To","Kumar Sanu","Pop","Happy","India",0.55,0.60,0.72,92),
    ("Pehla Nasha","Udit Narayan","Pop","Happy","India",0.52,0.58,0.75,90),
    ("Meri Mehbooba","Udit Narayan","Pop","Happy","India",0.56,0.60,0.74,94),
    ("Dil To Pagal Hai","Lata Mangeshkar","Pop","Happy","India",0.50,0.55,0.72,88),
    ("Lag Ja Gale","Lata Mangeshkar","Classical","Sad","India",0.22,0.28,0.18,58),
    ("Ajeeb Dastan Hai Yeh","Lata Mangeshkar","Classical","Sad","India",0.20,0.26,0.16,55),
    ("Tere Bina Zindagi","Kishore Kumar","Pop","Sad","India",0.28,0.35,0.20,70),
    ("Pal Pal Dil Ke Paas","Kishore Kumar","Pop","Happy","India",0.55,0.60,0.74,92),
    ("Kuch To Log Kahenge","Kishore Kumar","Pop","Relax","India",0.42,0.48,0.60,84),
    ("Roop Tera Mastana","Kishore Kumar","Pop","Happy","India",0.60,0.65,0.80,98),
    ("Yeh Shaam Mastani","Kishore Kumar","Pop","Happy","India",0.58,0.62,0.78,95),
    ("Mere Naina Sawan Bhadon","Kishore Kumar","Classical","Sad","India",0.30,0.36,0.22,68),
    # ARMAAN MALIK
    ("Bol Do Na Zara","Armaan Malik","Pop","Relax","India",0.40,0.45,0.50,80),
    ("Main Hoon Hero Tera","Armaan Malik","Pop","Happy","India",0.65,0.70,0.78,102),
    ("Woh Pehli Baar","Armaan Malik","Pop","Happy","India",0.55,0.60,0.72,92),
    ("Hasi","Armaan Malik","Pop","Happy","India",0.52,0.58,0.70,90),
    ("Baarish","Armaan Malik","Pop","Sad","India",0.35,0.40,0.28,72),
    # ATIF ASLAM
    ("Tere Sang Yaara","Atif Aslam","Pop","Happy","India",0.58,0.62,0.74,94),
    ("Pehli Dafa","Atif Aslam","Pop","Happy","India",0.52,0.58,0.70,90),
    ("Tu Jaane Na","Atif Aslam","Pop","Sad","India",0.32,0.40,0.22,70),
    ("Jeena Jeena","Atif Aslam","Pop","Happy","India",0.60,0.65,0.76,98),
    ("Tere Liye","Atif Aslam","Pop","Happy","India",0.55,0.60,0.72,90),
    ("Alvida","Atif Aslam","Pop","Sad","India",0.30,0.35,0.22,68),
    # BOLLYWOOD / REGIONAL HITS
    ("Dilbar Dilbar","Neha Kakkar","Pop","Party","India",0.82,0.85,0.80,115),
    ("Kar Gayi Chull","Badshah","Hip Hop","Party","India",0.85,0.88,0.82,118),
    ("Kala Chashma","Amar Arshi","Pop","Party","India",0.80,0.82,0.80,112),
    ("London Thumakda","Labh Janjua","Pop","Party","India",0.78,0.80,0.82,110),
    ("Naatu Naatu","Rahul Sipligunj","Pop","Party","India",0.90,0.92,0.88,125),
    ("Pushpa Pushpa","Fahad Faasil","Pop","Party","India",0.85,0.88,0.82,118),
    ("Srivalli","Sid Sriram","Pop","Sad","India",0.42,0.45,0.30,78),
    ("Oo Antava","Indravathi Chauhan","Pop","Party","India",0.82,0.85,0.80,115),
    ("Saami Saami","Mounika Reddy","Pop","Happy","India",0.72,0.75,0.78,108),
    ("Rowdy Baby","Dhanush","Pop","Party","India",0.80,0.82,0.80,112),
    ("Vaathi Coming","Anirudh Ravichander","Hip Hop","Party","India",0.85,0.88,0.82,118),
    ("Beast Mode","Anirudh Ravichander","Hip Hop","Focus","India",0.80,0.78,0.65,115),
    ("Arabic Kuthu","Anirudh Ravichander","Pop","Party","India",0.88,0.90,0.85,122),
    # AR RAHMAN
    ("Jai Ho","A.R. Rahman","Pop","Happy","India",0.78,0.80,0.82,115),
    ("Chaiyya Chaiyya","A.R. Rahman","Pop","Happy","India",0.80,0.82,0.80,118),
    ("Dil Se Re","A.R. Rahman","Pop","Focus","India",0.65,0.68,0.55,102),
    ("Roja","A.R. Rahman","Classical","Relax","India",0.40,0.42,0.65,78),
    ("O Saya","A.R. Rahman","Pop","Focus","India",0.70,0.72,0.55,108),
    ("Kehna Hi Kya","A.R. Rahman","Classical","Relax","India",0.38,0.40,0.65,75),
    ("Jai Ho You Are My Destiny","A.R. Rahman","Pop","Happy","India",0.75,0.78,0.78,112),
    ("Dil Hi Dil Mein","A.R. Rahman","Pop","Happy","India",0.62,0.65,0.75,98),
    # BADSHAH / NEHA KAKKAR / PUNJABI
    ("Paagal","Badshah","Hip Hop","Party","India",0.85,0.88,0.80,118),
    ("Genda Phool","Badshah","Hip Hop","Party","India",0.82,0.85,0.80,112),
    ("DJ Waley Babu","Badshah","Hip Hop","Party","India",0.88,0.90,0.82,122),
    ("Saturday Saturday","Badshah","Hip Hop","Party","India",0.82,0.85,0.78,115),
    ("Abhi Toh Party","Neha Kakkar","Pop","Party","India",0.80,0.82,0.82,112),
    ("Aankh Maare","Neha Kakkar","Pop","Party","India",0.82,0.85,0.80,115),
    ("Mile Ho Tum","Neha Kakkar","Pop","Happy","India",0.60,0.65,0.78,98),
    ("Nikle Currant","Neha Kakkar","Pop","Party","India",0.80,0.82,0.78,112),
    ("Desi Beat","Jazzy B","Bhangra","Party","India",0.85,0.88,0.85,120),
    ("Tunak Tunak Tun","Daler Mehndi","Bhangra","Party","India",0.88,0.90,0.88,125),
    ("Mundian To Bach Ke","Panjabi MC","Bhangra","Party","India",0.88,0.90,0.80,128),
    # KAILASH KHER / SUFI
    ("Ik Onkar","Harshdeep Kaur","Sufi","Relax","India",0.30,0.35,0.62,65),
    ("Afreen Afreen","Rahat Fateh Ali Khan","Sufi","Relax","India",0.28,0.32,0.65,60),
    ("Chaap Tilak","Abida Parveen","Sufi","Relax","India",0.25,0.30,0.68,58),
    ("Mast Qalandar","Nusrat Fateh Ali Khan","Sufi","Party","India",0.75,0.72,0.80,108),
    ("Mere Rashke Qamar","Rahat Fateh Ali Khan","Sufi","Happy","India",0.55,0.58,0.72,92),
    ("Nagare Nagare","Kailash Kher","Sufi","Party","India",0.75,0.78,0.78,108),
    ("Teri Deewani","Kailash Kher","Sufi","Happy","India",0.55,0.58,0.72,92),
    ("Allah Ke Bande","Kailash Kher","Sufi","Happy","India",0.52,0.55,0.70,88),
    # JUBIN NAUTIYAL / VISHAL MISHRA
    ("Raataan Lambiyan","Jubin Nautiyal","Pop","Happy","India",0.58,0.62,0.72,94),
    ("Tum Kab Aao Ge","Jubin Nautiyal","Pop","Sad","India",0.35,0.40,0.28,72),
    ("Pehle Bhi Main","Vishal Mishra","Pop","Happy","India",0.60,0.65,0.74,96),
    ("Tumhi Ho Bandhu","Kavita Seth","Pop","Happy","India",0.62,0.68,0.80,100),
    # ── THE WEEKND ───────────────────────────────────────────────
    ("Blinding Lights","The Weeknd","Pop","Party","USA",0.90,0.80,0.70,171),
    ("Starboy","The Weeknd","Pop","Focus","USA",0.78,0.76,0.50,186),
    ("Save Your Tears","The Weeknd","Pop","Sad","USA",0.65,0.72,0.55,118),
    ("After Hours","The Weeknd","Pop","Sad","USA",0.58,0.65,0.35,108),
    ("Can't Feel My Face","The Weeknd","Pop","Party","USA",0.80,0.78,0.65,170),
    ("The Hills","The Weeknd","Pop","Focus","USA",0.72,0.68,0.40,130),
    ("Call Out My Name","The Weeknd","Pop","Sad","USA",0.55,0.60,0.30,105),
    # ED SHEERAN
    ("Shape of You","Ed Sheeran","Pop","Happy","UK",0.65,0.83,0.93,96),
    ("Perfect","Ed Sheeran","Pop","Happy","UK",0.45,0.48,0.75,95),
    ("Thinking Out Loud","Ed Sheeran","Pop","Happy","UK",0.48,0.52,0.78,79),
    ("Photograph","Ed Sheeran","Pop","Sad","UK",0.52,0.55,0.60,108),
    ("Bad Habits","Ed Sheeran","Pop","Party","UK",0.80,0.80,0.70,126),
    ("Shivers","Ed Sheeran","Pop","Party","UK",0.82,0.82,0.72,142),
    ("Castle on the Hill","Ed Sheeran","Rock","Happy","UK",0.70,0.65,0.72,130),
    ("Galway Girl","Ed Sheeran","Pop","Party","UK",0.80,0.78,0.80,132),
    # TAYLOR SWIFT
    ("Anti-Hero","Taylor Swift","Pop","Happy","USA",0.68,0.72,0.55,97),
    ("Shake It Off","Taylor Swift","Pop","Party","USA",0.82,0.85,0.90,160),
    ("Blank Space","Taylor Swift","Pop","Happy","USA",0.68,0.72,0.60,96),
    ("Love Story","Taylor Swift","Pop","Happy","USA",0.62,0.65,0.80,119),
    ("You Belong With Me","Taylor Swift","Pop","Happy","USA",0.60,0.65,0.80,125),
    ("Wildest Dreams","Taylor Swift","Pop","Sad","USA",0.55,0.60,0.45,135),
    ("Cruel Summer","Taylor Swift","Pop","Party","USA",0.70,0.72,0.65,170),
    ("Cardigan","Taylor Swift","Pop","Sad","USA",0.38,0.45,0.40,118),
    ("Lover","Taylor Swift","Pop","Happy","USA",0.52,0.56,0.82,68),
    # ADELE
    ("Rolling in the Deep","Adele","Pop","Focus","UK",0.78,0.69,0.52,105),
    ("Someone Like You","Adele","Pop","Sad","UK",0.30,0.32,0.25,68),
    ("Hello","Adele","Pop","Sad","UK",0.42,0.45,0.30,80),
    ("Skyfall","Adele","Pop","Focus","UK",0.55,0.50,0.35,78),
    ("Set Fire to the Rain","Adele","Pop","Focus","UK",0.68,0.62,0.45,108),
    ("Easy On Me","Adele","Pop","Sad","UK",0.35,0.38,0.28,64),
    # DRAKE
    ("God's Plan","Drake","Hip Hop","Happy","USA",0.45,0.75,0.44,77),
    ("Hotline Bling","Drake","Hip Hop","Happy","USA",0.48,0.70,0.52,135),
    ("One Dance","Drake","R&B","Relax","USA",0.62,0.78,0.50,104),
    ("In My Feelings","Drake","Hip Hop","Happy","USA",0.62,0.80,0.55,92),
    ("Nonstop","Drake","Hip Hop","Focus","USA",0.68,0.78,0.48,130),
    ("Rich Flex","Drake","Hip Hop","Party","USA",0.75,0.80,0.52,130),
    ("Laugh Now Cry Later","Drake","Hip Hop","Happy","USA",0.65,0.78,0.52,96),
    # BILLIE EILISH
    ("Bad Guy","Billie Eilish","Pop","Focus","USA",0.55,0.70,0.42,135),
    ("Therefore I Am","Billie Eilish","Pop","Focus","USA",0.52,0.68,0.40,128),
    ("Happier Than Ever","Billie Eilish","Pop","Sad","USA",0.48,0.55,0.35,70),
    ("Ocean Eyes","Billie Eilish","Pop","Sad","USA",0.32,0.38,0.40,80),
    ("Lovely","Billie Eilish","Pop","Sad","USA",0.28,0.35,0.30,115),
    # COLDPLAY
    ("Yellow","Coldplay","Rock","Happy","UK",0.55,0.50,0.68,174),
    ("The Scientist","Coldplay","Rock","Sad","UK",0.38,0.42,0.40,75),
    ("Fix You","Coldplay","Rock","Sad","UK",0.42,0.38,0.38,138),
    ("Viva la Vida","Coldplay","Rock","Happy","UK",0.65,0.60,0.65,138),
    ("A Sky Full of Stars","Coldplay","EDM","Party","UK",0.80,0.75,0.72,125),
    ("Paradise","Coldplay","Pop","Happy","UK",0.68,0.65,0.72,126),
    ("Magic","Coldplay","Pop","Relax","UK",0.55,0.58,0.65,118),
    ("Higher Power","Coldplay","Pop","Party","UK",0.75,0.75,0.72,135),
    # EMINEM
    ("Lose Yourself","Eminem","Hip Hop","Focus","USA",0.88,0.68,0.49,171),
    ("Rap God","Eminem","Hip Hop","Focus","USA",0.82,0.72,0.42,186),
    ("Without Me","Eminem","Hip Hop","Party","USA",0.78,0.75,0.55,170),
    ("Love the Way You Lie","Eminem","Hip Hop","Sad","USA",0.70,0.65,0.38,87),
    ("Stan","Eminem","Hip Hop","Sad","USA",0.60,0.60,0.32,75),
    ("Not Afraid","Eminem","Hip Hop","Focus","USA",0.80,0.70,0.48,88),
    ("Mockingbird","Eminem","Hip Hop","Sad","USA",0.55,0.58,0.35,75),
    # RIHANNA
    ("Umbrella","Rihanna","Pop","Party","USA",0.78,0.78,0.65,125),
    ("Diamonds","Rihanna","Pop","Happy","USA",0.62,0.65,0.72,125),
    ("We Found Love","Rihanna","EDM","Party","USA",0.82,0.82,0.65,128),
    ("Work","Rihanna","R&B","Party","USA",0.70,0.80,0.55,96),
    ("Love on the Brain","Rihanna","R&B","Happy","USA",0.60,0.62,0.68,106),
    # BEYONCE
    ("Crazy in Love","Beyoncé","R&B","Party","USA",0.80,0.82,0.72,100),
    ("Halo","Beyoncé","Pop","Happy","USA",0.58,0.55,0.78,84),
    ("Single Ladies","Beyoncé","R&B","Party","USA",0.82,0.85,0.72,120),
    ("Irreplaceable","Beyoncé","R&B","Focus","USA",0.62,0.65,0.52,95),
    ("Love on Top","Beyoncé","R&B","Happy","USA",0.72,0.78,0.85,125),
    # QUEEN
    ("Bohemian Rhapsody","Queen","Rock","Focus","UK",0.70,0.50,0.55,144),
    ("Don't Stop Me Now","Queen","Rock","Party","UK",0.82,0.78,0.82,156),
    ("We Will Rock You","Queen","Rock","Party","UK",0.85,0.72,0.70,82),
    ("We Are the Champions","Queen","Rock","Happy","UK",0.75,0.62,0.78,63),
    ("Another One Bites the Dust","Queen","Rock","Party","UK",0.80,0.80,0.65,110),
    # MICHAEL JACKSON
    ("Thriller","Michael Jackson","Pop","Party","USA",0.78,0.80,0.62,138),
    ("Billie Jean","Michael Jackson","Pop","Focus","USA",0.82,0.80,0.55,118),
    ("Beat It","Michael Jackson","Rock","Focus","USA",0.80,0.75,0.58,139),
    ("Smooth Criminal","Michael Jackson","Pop","Focus","USA",0.82,0.82,0.58,119),
    ("Man in the Mirror","Michael Jackson","Pop","Happy","USA",0.55,0.55,0.75,100),
    ("Black or White","Michael Jackson","Pop","Happy","USA",0.72,0.70,0.75,122),
    # BRUNO MARS
    ("Uptown Funk","Bruno Mars","Funk","Party","USA",0.88,0.88,0.80,115),
    ("Just the Way You Are","Bruno Mars","Pop","Happy","USA",0.58,0.60,0.82,109),
    ("Grenade","Bruno Mars","Pop","Sad","USA",0.62,0.65,0.38,110),
    ("Locked Out of Heaven","Bruno Mars","Pop","Party","USA",0.80,0.80,0.78,144),
    ("Treasure","Bruno Mars","Funk","Party","USA",0.80,0.85,0.85,102),
    ("That's What I Like","Bruno Mars","Funk","Party","USA",0.80,0.85,0.80,124),
    # JUSTIN BIEBER
    ("Sorry","Justin Bieber","Pop","Happy","USA",0.72,0.78,0.70,100),
    ("Love Yourself","Justin Bieber","Pop","Happy","USA",0.55,0.62,0.72,102),
    ("Baby","Justin Bieber","Pop","Happy","USA",0.68,0.72,0.82,130),
    ("Peaches","Justin Bieber","R&B","Relax","USA",0.52,0.58,0.65,90),
    ("Ghost","Justin Bieber","Pop","Sad","USA",0.45,0.50,0.40,95),
    ("Stay","Justin Bieber","Pop","Happy","USA",0.62,0.65,0.68,170),
    # DUA LIPA
    ("Levitating","Dua Lipa","Pop","Party","UK",0.80,0.82,0.78,103),
    ("Don't Start Now","Dua Lipa","Pop","Happy","UK",0.72,0.78,0.72,124),
    ("Physical","Dua Lipa","Pop","Party","UK",0.80,0.82,0.72,122),
    ("New Rules","Dua Lipa","Pop","Focus","UK",0.72,0.76,0.60,116),
    ("One Kiss","Dua Lipa","Pop","Party","UK",0.78,0.80,0.72,121),
    # ARIANA GRANDE
    ("Thank U Next","Ariana Grande","Pop","Happy","USA",0.65,0.72,0.72,107),
    ("7 Rings","Ariana Grande","Pop","Party","USA",0.68,0.75,0.68,140),
    ("Problem","Ariana Grande","Pop","Happy","USA",0.72,0.78,0.72,128),
    ("Into You","Ariana Grande","Pop","Party","USA",0.80,0.80,0.68,128),
    ("Positions","Ariana Grande","R&B","Relax","USA",0.55,0.62,0.62,144),
    # BTS
    ("Dynamite","BTS","Pop","Party","Korea",0.77,0.74,0.74,114),
    ("Butter","BTS","Pop","Happy","Korea",0.76,0.82,0.74,110),
    ("DNA","BTS","Pop","Happy","Korea",0.78,0.80,0.72,126),
    ("Boy With Luv","BTS","Pop","Happy","Korea",0.78,0.82,0.78,134),
    ("Fake Love","BTS","Pop","Sad","Korea",0.65,0.68,0.38,124),
    ("Spring Day","BTS","Pop","Sad","Korea",0.52,0.58,0.45,120),
    ("Permission to Dance","BTS","Pop","Party","Korea",0.78,0.80,0.80,128),
    # BLACKPINK
    ("How You Like That","BLACKPINK","Pop","Party","Korea",0.80,0.82,0.68,130),
    ("DDU-DU DDU-DU","BLACKPINK","Pop","Focus","Korea",0.78,0.80,0.55,126),
    ("Kill This Love","BLACKPINK","Pop","Focus","Korea",0.82,0.78,0.52,140),
    ("Lovesick Girls","BLACKPINK","Pop","Sad","Korea",0.65,0.68,0.48,118),
    # JAZZ / CLASSICAL
    ("Take Five","Dave Brubeck","Jazz","Relax","USA",0.30,0.40,0.60,174),
    ("So What","Miles Davis","Jazz","Focus","USA",0.35,0.42,0.55,136),
    ("Fly Me to the Moon","Frank Sinatra","Jazz","Happy","USA",0.42,0.50,0.82,120),
    ("My Way","Frank Sinatra","Pop","Relax","USA",0.40,0.45,0.72,75),
    ("What a Wonderful World","Louis Armstrong","Jazz","Happy","USA",0.22,0.30,0.82,72),
    ("Clair de Lune","Debussy","Classical","Relax","UK",0.10,0.20,0.50,65),
    ("Canon in D","Pachelbel","Classical","Focus","UK",0.12,0.25,0.60,98),
    ("Moonlight Sonata","Beethoven","Classical","Sad","UK",0.15,0.22,0.30,58),
    ("Four Seasons","Vivaldi","Classical","Happy","UK",0.45,0.40,0.72,130),
    # EDM
    ("Titanium","David Guetta","EDM","Party","USA",0.78,0.71,0.42,126),
    ("Levels","Avicii","EDM","Party","UK",0.82,0.73,0.88,126),
    ("Wake Me Up","Avicii","EDM","Happy","UK",0.78,0.72,0.80,124),
    ("Animals","Martin Garrix","EDM","Party","UK",0.88,0.80,0.65,128),
    ("Closer","The Chainsmokers","Pop","Happy","USA",0.68,0.72,0.72,95),
    ("Don't Let Me Down","The Chainsmokers","EDM","Focus","USA",0.72,0.70,0.55,160),
    ("Happier","Marshmello","EDM","Happy","USA",0.68,0.72,0.75,100),
    ("Alone","Marshmello","EDM","Focus","USA",0.80,0.78,0.60,128),
    ("Turn Down for What","DJ Snake","EDM","Party","USA",0.90,0.88,0.62,100),
    ("Taki Taki","DJ Snake","EDM","Party","USA",0.85,0.88,0.72,130),
    ("Lean On","Major Lazer","EDM","Party","USA",0.80,0.80,0.72,98),
    ("On My Way","Alan Walker","EDM","Happy","Norway",0.72,0.75,0.72,104),
    ("Faded","Alan Walker","EDM","Sad","Norway",0.62,0.65,0.45,90),
    # LATIN
    ("Despacito","Luis Fonsi","Pop","Party","USA",0.65,0.69,0.82,89),
    ("Gasolina","Daddy Yankee","Reggaeton","Party","USA",0.82,0.88,0.75,108),
    ("Waka Waka","Shakira","Pop","Party","USA",0.80,0.82,0.85,118),
    ("Hips Don't Lie","Shakira","Pop","Party","USA",0.80,0.85,0.82,100),
    # ROCK CLASSICS
    ("Hotel California","Eagles","Rock","Relax","USA",0.55,0.55,0.60,75),
    ("Stairway to Heaven","Led Zeppelin","Rock","Relax","UK",0.60,0.50,0.60,82),
    ("Smells Like Teen Spirit","Nirvana","Rock","Focus","USA",0.78,0.68,0.50,117),
    ("Eye of the Tiger","Survivor","Rock","Focus","USA",0.78,0.70,0.62,109),
    ("Livin on a Prayer","Bon Jovi","Rock","Happy","USA",0.78,0.68,0.75,123),
    ("Summer of 69","Bryan Adams","Rock","Happy","USA",0.72,0.65,0.80,136),
    ("Wonderwall","Oasis","Rock","Happy","UK",0.52,0.50,0.68,87),
    ("Mr. Brightside","The Killers","Rock","Focus","UK",0.78,0.72,0.55,148),
    ("Seven Nation Army","The White Stripes","Rock","Focus","USA",0.70,0.65,0.50,124),
    ("Creep","Radiohead","Rock","Sad","UK",0.52,0.48,0.32,92),
    ("Sweet Child O Mine","Guns N Roses","Rock","Happy","USA",0.72,0.62,0.72,125),
    ("Don't Stop Believin","Journey","Rock","Happy","USA",0.72,0.65,0.75,119),
    # HIP HOP
    ("HUMBLE","Kendrick Lamar","Hip Hop","Focus","USA",0.78,0.72,0.42,150),
    ("SICKO MODE","Travis Scott","Hip Hop","Focus","USA",0.82,0.80,0.42,155),
    ("Rockstar","Post Malone","Hip Hop","Focus","USA",0.72,0.70,0.38,160),
    ("Sunflower","Post Malone","Pop","Happy","USA",0.58,0.65,0.72,94),
    ("In Da Club","50 Cent","Hip Hop","Party","USA",0.82,0.82,0.58,102),
    ("California Gurls","Katy Perry","Pop","Party","USA",0.80,0.82,0.82,120),
    ("Roar","Katy Perry","Pop","Happy","USA",0.72,0.70,0.80,130),
    ("Firework","Katy Perry","Pop","Happy","USA",0.68,0.65,0.82,124),
    # MAROON 5 / ONEREPUBLIC / OTHERS
    ("Moves Like Jagger","Maroon 5","Pop","Party","USA",0.78,0.80,0.72,128),
    ("She Will Be Loved","Maroon 5","Pop","Happy","USA",0.55,0.60,0.72,104),
    ("Sugar","Maroon 5","Pop","Happy","USA",0.68,0.75,0.80,122),
    ("Counting Stars","OneRepublic","Pop","Happy","USA",0.68,0.65,0.72,122),
    ("Apologize","OneRepublic","Pop","Sad","USA",0.48,0.50,0.38,128),
    ("Zombie","The Cranberries","Rock","Focus","UK",0.68,0.60,0.42,118),
    ("Happy","Pharrell Williams","Pop","Happy","USA",0.68,0.85,0.96,160),
    ("Get Lucky","Daft Punk","Funk","Party","USA",0.78,0.82,0.80,116),
    ("Africa","Toto","Rock","Happy","USA",0.62,0.62,0.72,93),
    ("Take On Me","a-ha","Pop","Happy","Norway",0.68,0.70,0.78,170),
    # CLASSIC WESTERN POP
    ("Uptown Girl","Billy Joel","Pop","Happy","USA",0.70,0.72,0.82,148),
    ("Piano Man","Billy Joel","Rock","Relax","USA",0.45,0.50,0.68,90),
    ("Girls Just Want to Have Fun","Cyndi Lauper","Pop","Party","USA",0.75,0.75,0.85,120),
    ("Baby One More Time","Britney Spears","Pop","Party","USA",0.72,0.78,0.72,100),
    ("Toxic","Britney Spears","Pop","Party","USA",0.75,0.80,0.65,143),
    ("Since U Been Gone","Kelly Clarkson","Rock","Focus","USA",0.75,0.72,0.62,126),
    ("Beautiful","Christina Aguilera","Pop","Happy","USA",0.42,0.45,0.72,56),
    ("Crazy","Gnarls Barkley","Pop","Focus","USA",0.62,0.68,0.48,112),
    # WHITNEY / CELINE / ARETHA / SOUL
    ("I Will Always Love You","Whitney Houston","Pop","Sad","USA",0.45,0.40,0.55,66),
    ("I Wanna Dance with Somebody","Whitney Houston","Pop","Party","USA",0.78,0.82,0.85,118),
    ("My Heart Will Go On","Celine Dion","Pop","Sad","USA",0.38,0.35,0.45,66),
    ("The Power of Love","Celine Dion","Pop","Happy","USA",0.52,0.48,0.72,68),
    ("Respect","Aretha Franklin","Soul","Focus","USA",0.72,0.72,0.80,115),
    # RECENT / INDIE
    ("As It Was","Harry Styles","Pop","Sad","UK",0.58,0.62,0.48,174),
    ("Watermelon Sugar","Harry Styles","Pop","Happy","UK",0.68,0.72,0.82,95),
    ("Heat Waves","Glass Animals","Indie","Sad","UK",0.55,0.62,0.42,80),
    ("drivers license","Olivia Rodrigo","Pop","Sad","USA",0.43,0.45,0.32,174),
    ("good 4 u","Olivia Rodrigo","Pop","Focus","USA",0.68,0.70,0.55,166),
    ("Vampire","Olivia Rodrigo","Pop","Sad","USA",0.52,0.55,0.40,138),
    ("Let Her Go","Passenger","Pop","Sad","UK",0.42,0.48,0.38,76),
    ("Ho Hey","The Lumineers","Indie","Happy","USA",0.55,0.58,0.75,102),
    # R&B / SOUL
    ("No Ordinary Love","Sade","R&B","Relax","UK",0.38,0.45,0.48,80),
    ("Smooth Operator","Sade","R&B","Relax","UK",0.40,0.48,0.55,84),
    ("Essence","Wizkid","Afrobeat","Relax","USA",0.62,0.68,0.72,100),
    ("Jerusalema","Master KG","Afrobeat","Party","South Africa",0.80,0.85,0.82,118),
    # JAPANESE POP
    ("Sakura","Ikimono Gakari","Pop","Happy","Japan",0.60,0.65,0.80,130),
    ("Lemon","Kenshi Yonezu","Pop","Sad","Japan",0.50,0.55,0.15,90),
    ("Pretender","Official HIGE DANdism","Rock","Focus","Japan",0.65,0.60,0.45,120),
    ("Gurenge","LiSA","Rock","Focus","Japan",0.78,0.72,0.55,185),
    ("Idol","Yoasobi","Pop","Happy","Japan",0.80,0.82,0.75,168),
    ("Yoru ni Kakeru","Yoasobi","Pop","Focus","Japan",0.72,0.75,0.55,132),
    ("Plastic Love","Mariya Takeuchi","Pop","Happy","Japan",0.65,0.70,0.80,118),
    ("Usseewa","Ado","Rock","Focus","Japan",0.82,0.78,0.48,174),
]

ALL_SONGS = [s(i+1, *row) for i, row in enumerate(_raw)]

GENRES    = sorted(set(x["genre"] for x in ALL_SONGS))
MOODS     = ["Happy", "Sad", "Relax", "Focus", "Party"]
COUNTRIES = sorted(set(x["country"] for x in ALL_SONGS))

# ── ML ──────────────────────────────────────────────────────────
class Recommender:
    def __init__(self):
        self.le_g = LabelEncoder().fit(GENRES)
        self.le_m = LabelEncoder().fit(MOODS)
        self.le_c = LabelEncoder().fit(COUNTRIES)
        self.le_a = LabelEncoder().fit(sorted(set(x["artist"] for x in ALL_SONGS)))
        self.F = np.array([self._v(x) for x in ALL_SONGS])
        self.knn = NearestNeighbors(n_neighbors=10, metric="cosine", algorithm="brute")
        self.knn.fit(self.F)

    def _v(self, x):
        g = self.le_g.transform([x["genre"]])[0]   / max(len(GENRES)-1,1)
        m = self.le_m.transform([x["mood"]])[0]    / max(len(MOODS)-1,1)
        c = self.le_c.transform([x["country"]])[0] / max(len(COUNTRIES)-1,1)
        a = self.le_a.transform([x["artist"]])[0]  / max(len(self.le_a.classes_)-1,1)
        return [g*3,m*2.5,c*1,a*2,x["energy"]*2,x["danceability"]*1.5,x["valence"]*1.5,x["tempo"]/200]

    def similar(self, sid, n=8):
        idx = next((i for i,x in enumerate(ALL_SONGS) if x["id"]==sid), None)
        if idx is None: return []
        dist,inds = self.knn.kneighbors(self.F[idx].reshape(1,-1))
        out=[]
        for i,d in zip(inds[0],dist[0]):
            if ALL_SONGS[i]["id"]!=sid:
                r=dict(ALL_SONGS[i]); r["similarity_score"]=round(float(1-d),3); out.append(r)
        return out[:n]

    def recommend(self, genre=None,mood=None,country=None,artist=None):
        def sc(x):
            v=0
            if genre   and x["genre"]  ==genre:   v+=3
            if mood    and x["mood"]   ==mood:     v+=2.5
            if country and x["country"]==country:  v+=1
            if artist  and x["artist"] ==artist:   v+=2
            return v
        f=[x for x in ALL_SONGS if
           (not genre   or x["genre"]  ==genre)  and
           (not mood    or x["mood"]   ==mood)    and
           (not country or x["country"]==country) and
           (not artist  or x["artist"] ==artist)]
        return sorted(f,key=sc,reverse=True)[:8]

REC = Recommender()

# ── ROUTES ──────────────────────────────────────────────────────
@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/songs")
def api_songs(): return jsonify({"songs":ALL_SONGS,"genres":GENRES,"moods":MOODS,"countries":COUNTRIES})

@app.route("/api/similar/<sid>")
def api_similar(sid):
    return jsonify({"similar":REC.similar(sid,int(request.args.get("n",8))),"algorithm":"KNN Cosine"})

@app.route("/api/recommend")
def api_recommend():
    return jsonify({"recommendations":REC.recommend(
        request.args.get("genre"),request.args.get("mood"),
        request.args.get("country"),request.args.get("artist"))})

@app.route("/api/mood-vector/<sid>")
def api_mood(sid):
    x=next((y for y in ALL_SONGS if y["id"]==sid),None)
    if not x: return jsonify({}),404
    return jsonify({"features":{k:x[k] for k in ["energy","danceability","valence","tempo"]}})

@app.route("/api/artists-by-country/<country>")
def api_artists(country):
    return jsonify({"artists":sorted(set(x["artist"] for x in ALL_SONGS if x["country"]==country))})

@app.route("/api/search")
def api_search():
    q=request.args.get("q","").lower()
    if not q: return jsonify({"results":[]})
    return jsonify({"results":[x for x in ALL_SONGS
        if q in x["title"].lower() or q in x["artist"].lower()][:12]})

import json, os, hashlib, time

PROFILES_FILE = os.path.join(os.path.dirname(__file__), "profiles.json")

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE) as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ── AUTH & PROFILE ROUTES ──────────────────────────────────────

@app.route("/api/register", methods=["POST"])
def api_register():
    d = request.get_json() or {}
    email    = (d.get("email") or "").strip().lower()
    password = d.get("password", "")
    name     = (d.get("name") or "").strip()
    if not email or not password or not name:
        return jsonify({"success": False, "error": "Name, email and password are required"}), 400
    profiles = load_profiles()
    if email in profiles:
        return jsonify({"success": False, "error": "An account with this email already exists"}), 409
    profiles[email] = {
        "email": email,
        "password": hash_pw(password),
        "name": name,
        "bio": d.get("bio", ""),
        "avatar_color": d.get("avatar_color", "#a855f7"),
        "fav_genre": d.get("fav_genre", ""),
        "fav_mood": d.get("fav_mood", ""),
        "location": d.get("location", ""),
        "created_at": int(time.time()),
        "liked_songs": [],
        "playlists": [],
    }
    save_profiles(profiles)
    session["user"] = email
    p = dict(profiles[email]); p.pop("password")
    return jsonify({"success": True, "profile": p})

@app.route("/api/login", methods=["POST"])
def api_login():
    d = request.get_json() or {}
    email    = (d.get("email") or "").strip().lower()
    password = d.get("password", "")
    profiles = load_profiles()
    if email in profiles and profiles[email]["password"] == hash_pw(password):
        session["user"] = email
        p = dict(profiles[email]); p.pop("password")
        return jsonify({"success": True, "profile": p})
    # Demo fallback: allow any login, create guest profile
    if email and password:
        if email not in profiles:
            profiles[email] = {
                "email": email, "password": hash_pw(password),
                "name": email.split("@")[0].title(), "bio": "",
                "avatar_color": "#a855f7", "fav_genre": "", "fav_mood": "",
                "location": "", "created_at": int(time.time()),
                "liked_songs": [], "playlists": [],
            }
            save_profiles(profiles)
        session["user"] = email
        p = dict(profiles[email]); p.pop("password")
        return jsonify({"success": True, "profile": p})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop("user", None)
    return jsonify({"success": True})

@app.route("/api/profile", methods=["GET"])
def api_get_profile():
    email = session.get("user")
    if not email: return jsonify({"error": "Not logged in"}), 401
    profiles = load_profiles()
    if email not in profiles: return jsonify({"error": "Profile not found"}), 404
    p = dict(profiles[email]); p.pop("password")
    return jsonify({"profile": p})

@app.route("/api/profile", methods=["PUT"])
def api_update_profile():
    email = session.get("user")
    if not email: return jsonify({"error": "Not logged in"}), 401
    profiles = load_profiles()
    if email not in profiles: return jsonify({"error": "Profile not found"}), 404
    d = request.get_json() or {}
    allowed = ["name","bio","avatar_color","fav_genre","fav_mood","location"]
    for k in allowed:
        if k in d: profiles[email][k] = d[k]
    # Handle password change
    if d.get("new_password") and d.get("current_password"):
        if profiles[email]["password"] != hash_pw(d["current_password"]):
            return jsonify({"success": False, "error": "Current password is incorrect"}), 400
        profiles[email]["password"] = hash_pw(d["new_password"])
    save_profiles(profiles)
    p = dict(profiles[email]); p.pop("password")
    return jsonify({"success": True, "profile": p})

@app.route("/api/profile/data", methods=["PUT"])
def api_save_user_data():
    """Save liked songs + playlists for the logged-in user."""
    email = session.get("user")
    if not email: return jsonify({"error": "Not logged in"}), 401
    profiles = load_profiles()
    if email not in profiles: return jsonify({"error": "Not found"}), 404
    d = request.get_json() or {}
    if "liked_songs" in d: profiles[email]["liked_songs"] = d["liked_songs"]
    if "playlists"   in d: profiles[email]["playlists"]   = d["playlists"]
    save_profiles(profiles)
    return jsonify({"success": True})

if __name__ == "__main__":
    print(f"✓ Loaded {len(ALL_SONGS)} songs")
    app.run(debug=True, port=5000)
