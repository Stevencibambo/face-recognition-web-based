<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="icon" type="image/ico" href="images/access/icon_1.png" />
    <link rel="stylesheet" href="css/bootstrap.min.css" />
    <link rel="stylesheet" href="css/style.css" />
    <title>Face registration</title>
</head>

    <body class="container-fuild">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="#"><h1>Register new face</h1></a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <!-- <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a> -->
                    </li>
                </ul>
                <form class="form-inline my-2 my-lg-0">
                    <a href= "../" type="button" class="btn btn-secondary btn-lg">Home</a>&nbsp;&nbsp;
                    <a class="btn btn-primary btn-lg" href="../verify/" role='button'>Face verification</a>
                </form>
            </div>
        </nav>
        <div class="container">
            <div class="row" id="main-div">
                <div class="col-8">
                    <div class="row option-btn">
                        <div class="col-8">
                            <div class="media-div" style="position:relative">
                                <video id="video" poster="images/access/play-image.png" style="border:1px solid black" width="640" height="480" autoplay muted playsinline></video>
                                <canvas id="canvas" />
                            </div>
                        </div>
                    </div>
                    <div class="row option-btn">
                        <div class="col-12">
                            <button type="button" name="capture" class="btn btn-primary" id="capture">Start camera</button>
                        </div>
                    </div>
                    <div>
                    </div>
                </div>
                <div class="col-4">

                </div>
            </div>
        </div>
        <div class="container-fluid">
            <div class="row">
                <div class="col-12" id="footer">
                    <span>all right reseved &copy; 2021</span>
                </div>
            </div>
        </div>
    </body>
    <script defer src="js/face_api.min.js"></script>
    <script defer src="js/script.js"></script>
</html>
