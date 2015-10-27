/**
 * Created by vitaly on 9/5/15.
 */

var feed = {
    player_selector: null,
    player_paused: true,
    image_height_lim: 280,

    init: function (){

        var that = this;

        this.player_selector = $("#html5_player");

        // ended callback
        this.player_selector.bind("ended",function(){
            $(".audio").removeClass("playing");
            that.player_paused = true;

            that.player_selector.attr('src', '');
        });

        $(".image > img").bind('load', function (){

            var image = $(this);
            var img_height = image.height();

            if (img_height > that.image_height_lim){
                image.css({"margin-top": -((img_height-that.image_height_lim)/2)})
            }

        });
    },

    expand: function (elem){
        $(elem).animate({"max-height": "100%"}, 150);
        $(elem).find('img').animate({"margin-top": 0}, 150);
    },

    playAudio: function(elem){
        var audio_elem = $(elem); //.childNodes[0];

        var audio_url = audio_elem.data("url");

        var old_url =  this.player_selector.attr("src");

        if (old_url == audio_url){

            var trigger_name = this.player_paused ? "play" : "pause";
            this.player_selector.trigger(trigger_name);

            this.player_paused = !this.player_paused;
            audio_elem.toggleClass("playing");
        } else {
            $(".audio").removeClass("playing");

            this.player_selector.attr("src", audio_url).trigger("play");
            this.player_paused = false;

            audio_elem.addClass("playing");
        }
    }
};


$(document).ready(function (){
    feed.init();
});

