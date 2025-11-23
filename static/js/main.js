 $(document).ready(function() {
    // Preloader
    // $(".preloader").fadeOut("slow");
    $('.preloader').addClass('fade-out');
    setTimeout(function() {
        $('.preloader').fadeOut();
    }, 500);
    $(window).on('load', function() {
        $('.preloader').addClass('fade-out');
        // $(".preloader").fadeOut("slow");
    });
    
    // Sticky Header
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 100) {
            $('.main-header').addClass('sticky');
        } else {
            $('.main-header').removeClass('sticky');
        }
    });
    
    // Mobile Menu Toggle
    $('.menu-toggle').on('click', function() {
        $('.nav-menu').toggleClass('active');
        $(this).toggleClass('active');
    });
    
    // Close mobile menu when clicking on a link
    $('.nav-menu li a').on('click', function() {
        $('.nav-menu').removeClass('active');
        $('.menu-toggle').removeClass('active');
    });
    
    // Back to Top Button
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').addClass('active');
        } else {
            $('.back-to-top').removeClass('active');
        }
    });
    
    $('.back-to-top').on('click', function() {
        $('html, body').animate({scrollTop: 0}, 800);
        return false;
    });
    
    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        var target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 80
            }, 800);
        }
    });
    
    // Newsletter form submission
    $('.newsletter-form').on('submit', function(e) {
        e.preventDefault();
        var email = $(this).find('input[type="email"]').val();
        
        // Here you would typically send the email to your server
        // For demo purposes, we'll just show a success message
        alert('Thank you for subscribing with: ' + email);
        $(this)[0].reset();
    });
    
    // Animation on scroll
    $(window).on('scroll', function() {
        $('.sector-card, .benefit-card, .testimonial-card').each(function() {
            var elementPos = $(this).offset().top;
            var topOfWindow = $(window).scrollTop();
            var windowHeight = $(window).height();
            
            if (elementPos < topOfWindow + windowHeight - 100) {
                $(this).addClass('animate');
            }
        });
    });
    document.querySelectorAll('.step').forEach((step, index) => {
      step.addEventListener('click', () => {
        document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
        step.classList.add('active');
      });
    });
});
