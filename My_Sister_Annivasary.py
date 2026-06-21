<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Happy Birthday My Love & Wife❤️</title>

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family: 'Poppins', sans-serif;
}

body{
    height:100vh;
    overflow:hidden;
    background:linear-gradient(135deg,#ff758c,#ff7eb3);
    display:flex;
    justify-content:center;
    align-items:center;
    text-align:center;
}

.container{
    z-index:10;
    color:white;
}

h1{
    font-size:4rem;
    animation: glow 2s infinite alternate;
}

@keyframes glow{
    from{
        text-shadow:0 0 10px #fff,
                    0 0 20px #fff,
                    0 0 30px #ff4da6;
    }
    to{
        text-shadow:0 0 20px #fff,
                    0 0 40px #ff4da6,
                    0 0 60px #ff4da6;
    }
}

.message{
    margin-top:20px;
    font-size:1.5rem;
    max-width:700px;
}

.photo{
    margin-top:25px;
}

.photo img{
    width:250px;
    height:250px;
    border-radius:50%;
    object-fit:cover;
    border:5px solid white;
    box-shadow:0 0 30px white;
}

.love{
    font-size:2rem;
    margin-top:20px;
    animation: heartbeat 1s infinite;
}

@keyframes heartbeat{
    0%{transform:scale(1);}
    50%{transform:scale(1.2);}
    100%{transform:scale(1);}
}

.balloon{
    position:absolute;
    bottom:-150px;
    width:60px;
    height:80px;
    border-radius:50%;
    animation: float 10s linear infinite;
}

.balloon::before{
    content:"";
    position:absolute;
    width:2px;
    height:100px;
    background:white;
    left:50%;
    top:80px;
}

@keyframes float{
    from{
        transform:translateY(0);
    }
    to{
        transform:translateY(-120vh);
    }
}

.heart{
    position:absolute;
    color:white;
    font-size:25px;
    animation: hearts 8s linear infinite;
}

@keyframes hearts{
    from{
        transform:translateY(100vh);
        opacity:1;
    }
    to{
        transform:translateY(-100vh);
        opacity:0;
    }
}
</style>
</head>

<body>

<div class="container">
    <h1>🎂 Happy Birthday My Love ❤️</h1>

    <div class="photo">
        <!-- Replace wife.jpg with your wife's image -->
        <img src="wife.jpg" alt="My Love">
    </div>

    <p class="message">
        Happy Birthday to the most beautiful woman in my life. ❤️<br><br>

        Ne enoda life vandhadhuku apram dhan enoda life avalo azhaga Change aatchu Thanks di my dr
        May your birthday be filled with joy, laughter, and all the love you deserve.

        I Love You Forever ❤️
    </p>

    <div class="love">💖 Forever Yours 💖</div>
</div>

<!-- Background Music -->
<audio autoplay loop>
    <source src="birthday.mp3" type="audio/mp3">
</audio>

<!-- Balloons -->
<div class="balloon" style="left:10%; background:red; animation-duration:8s;"></div>
<div class="balloon" style="left:25%; background:yellow; animation-duration:10s;"></div>
<div class="balloon" style="left:40%; background:blue; animation-duration:12s;"></div>
<div class="balloon" style="left:60%; background:green; animation-duration:9s;"></div>
<div class="balloon" style="left:80%; background:purple; animation-duration:11s;"></div>

<!-- Hearts -->
<div class="heart" style="left:15%;">❤️</div>
<div class="heart" style="left:30%; animation-delay:2s;">💖</div>
<div class="heart" style="left:50%; animation-delay:4s;">❤️</div>
<div class="heart" style="left:70%; animation-delay:1s;">💕</div>
<div class="heart" style="left:85%; animation-delay:3s;">💗</div>

</body>
</html>
