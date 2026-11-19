// Configuration pour les sections avec la classe ".dark"
$(".dark").each(function (index) {
  ScrollTrigger.create({
    trigger: $(this),
    start: "top 5%",
    end: "bottom 5%",
    onEnter: () => {
      $(".navbar_component").addClass("dark");
      $(".text-style-link.nav").addClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");



    },
    onEnterBack: () => {
      $("..navbar_component").addClass("dark");
      $(".text-style-link.nav").addClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");


    },
    onLeave: () => {
      $(".navbar_component").removeClass("dark");
      $(".text-style-link.nav").removeClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");
      
      },
    onLeaveBack: () => {
      $(".navbar_component").removeClass("dark");
      $(".text-style-link.nav").removeClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");
    }
  });
});

// Configuration pour les sections avec la classe ".light"
$(".light").each(function (index) {
  ScrollTrigger.create({
    trigger: $(this),
    start: "top 5%",
    end: "bottom 5%",
    onEnter: () => {
      $(".navbar_component").removeClass("dark");
      $(".text-style-link.nav").removeClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");
      },
    onEnterBack: () => {
      $(".navbar_component").removeClass("dark");
      $(".text-style-link.nav").removeClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");
      },
    onLeave: () => {
      $(".navbar_component").removeClass("dark");
      $(".text-style-link.nav").removeClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");
      },
    onLeaveBack: () => {
      $(".navbar_component").removeClass("dark");
      $(".text-style-link.nav").removeClass("dark");
      $(".button.nav").addClass("is-blur");
      $(".hover-link-mask").addClass("dark");
      $(".logo-name").addClass("dark");
      $(".navbar1_menu.is-page-height-tablet").addClass("dark");
      $(".menu-icon1_line-top").addClass("dark");
      $(".menu-icon1_line-middle").addClass("dark");
      $(".menu-icon1_line-bottom").addClass("dark");
      }
  });
});

document.addEventListener("DOMContentLoaded", function() {
    const nonCmsElement = document.getElementById("Non-Cms");
    const partnerGrid = document.getElementById("Partner-grid");
    const screenWidth = window.innerWidth;
    
    if (screenWidth > 767) {
      if (nonCmsElement && partnerGrid) {
        partnerGrid.appendChild(nonCmsElement);

        const cmsItems = partnerGrid.querySelectorAll('#partner-item');
        const numItems = cmsItems.length;

        let columnsToSpan = 1;

        if (numItems % 3 === 1) {
          columnsToSpan = 2;
        } else if (numItems % 3 === 2) {
          columnsToSpan = 1;
        } else if (numItems % 3 === 0) {
          columnsToSpan = 3;
        }

        nonCmsElement.style.gridColumn = `span ${columnsToSpan}`;
      }
    }
  });
