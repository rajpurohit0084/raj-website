#!/usr/bin/env python3
"""
Script to update all HTML pages with mobile sidebar functionality
"""

import os
import re

# List of HTML files to update (excluding index.html which is already updated)
html_files = [
    'about.html',
    'contact.html', 
    'products.html',
    'applications.html',
    'infrastructure.html',
    'limestone.html',
    'hydrated-lime-powder.html',
    'quick-lime-powder.html',
    'quick-lime-lump.html',
    'rajshree-minerals-brochure.html'
]

# Mobile sidebar CSS to add
mobile_sidebar_css = '''
        /* Premium Mobile Sidebar with Enhanced Effects */
        @media (max-width: 768px) {
          .sidebar {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
            padding: 25px 20px;
            width: 280px;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
          }

          .sidebar-links a {
            display: block;
            color: #ffffff !important;
            font-weight: 600;
            background: rgba(135, 206, 235, 0.15);
            margin: 12px 0;
            padding: 16px 20px;
            border-radius: 12px;
            position: relative;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            text-decoration: none;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
          }

          .sidebar-links a i {
            color: #ffffff !important;
            transition: all 0.3s ease;
          }

          .sidebar-links a:hover,
          .sidebar-links a:active {
            color: #ffffff !important;
            text-shadow: 0 0 8px rgba(135, 206, 235, 0.8), 0 0 16px rgba(135, 206, 235, 0.4);
            background: rgba(135, 206, 235, 0.25);
            transform: translateX(5px);
            box-shadow: 0 4px 20px rgba(135, 206, 235, 0.3);
            border-color: rgba(135, 206, 235, 0.4);
          }

          .sidebar-links a:hover i,
          .sidebar-links a:active i {
            color: #ffffff !important;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
          }

          .sidebar-links a::after {
            content: '';
            position: absolute;
            left: 20px;
            bottom: 12px;
            height: 3px;
            width: 0;
            background: linear-gradient(90deg, #87ceeb, #00bfff);
            box-shadow: 0 0 12px rgba(135, 206, 235, 0.8);
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 2px;
          }

          .sidebar-links a:hover::after,
          .sidebar-links a:active::after {
            width: 85%;
            box-shadow: 0 0 20px rgba(135, 206, 235, 1);
          }

          /* Enhanced active state */
          .sidebar-links .active a {
            color: #ffffff !important;
            background: rgba(135, 206, 235, 0.3);
            border-color: rgba(135, 206, 235, 0.6);
            box-shadow: 0 4px 25px rgba(135, 206, 235, 0.4);
          }

          .sidebar-links .active a i {
            color: #ffffff !important;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
          }

          .sidebar-links .active a::after {
            width: 85%;
            box-shadow: 0 0 20px rgba(135, 206, 235, 1);
          }
        }

        /* Mobile Sidebar Structure */
        @media (max-width: 600px) {
          .mobile-bottom-nav {
            display: flex !important;
          }
          body {
            padding-bottom: 60px !important;
          }
          .nav-btn.active, .nav-btn:active {
            color: #1565c0 !important;
            font-weight: 700;
            background: #e3f2fd;
            border-radius: 8px 8px 0 0;
          }
          
          /* Mobile menu animations */
          #mobileMenuOverlay {
            transform: translateX(-100%);
            transition: transform 0.3s ease-in-out;
          }
          
          #mobileMenuOverlay[style*="display: block"] {
            transform: translateX(0);
          }
          
          /* Premium Sidebar CSS */
          @media (min-width: 992px) {
            #mobileSidebar, #sidebarBackdrop {
              display: none !important;
            }
          }

          #sidebarBackdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(3px);
            opacity: 0;
            pointer-events: none;
            z-index: 998;
            transition: all 0.3s ease;
          }

          .sidebar {
            position: fixed;
            left: -270px;
            top: 0;
            width: 260px;
            height: 100vh;
            background: rgba(10, 20, 30, 0.7);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            z-index: 999;
            transition: all 0.4s ease;
            display: flex;
            flex-direction: column;
            padding: 20px 10px;
          }

          .sidebar.show {
            left: 0;
          }
          
          #sidebarBackdrop.show {
            opacity: 1;
            pointer-events: auto;
          }

          .sidebar .close-btn {
            font-size: 26px;
            color: #fff;
            align-self: flex-end;
            cursor: pointer;
            transition: transform 0.3s ease;
          }
          
          .sidebar .close-btn:hover {
            transform: rotate(90deg);
          }

          .sidebar-links {
            list-style: none;
            padding: 0;
            margin-top: 40px;
          }

          .sidebar-links li {
            margin: 15px 0;
          }

          .sidebar-links a {
            color: gold;
            text-decoration: none;
            font-size: 18px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s ease;
            letter-spacing: 0.5px;
          }

          .sidebar-links a:hover {
            color: #ffcc00;
            letter-spacing: 1.5px;
            text-shadow: 0 0 8px rgba(255, 215, 0, 0.7);
          }

          .sidebar-links .active a {
            color: #ffd700;
            font-weight: bold;
            border-left: 3px solid #ffd700;
            padding-left: 8px;
          }

          .sidebar-links a i {
            color: gold;
            transition: all 0.3s ease;
          }

          .sidebar-links a:hover i {
            filter: drop-shadow(0 0 6px gold);
          }

          .social-icons {
            margin-top: auto;
            display: flex;
            justify-content: space-around;
            padding: 15px 0;
          }

          .social-icons a i {
            font-size: 22px;
            color: #fff;
            transition: transform 0.3s, filter 0.3s;
          }
          
          .social-icons a:hover i {
            transform: scale(1.2);
            filter: drop-shadow(0 0 6px white);
          }
          
          /* Menu button icon transition */
          #menuIcon {
            transition: all 0.3s ease;
          }
          
          #mobileMenuBtn:hover #menuIcon {
            transform: scale(1.1);
          }
        }
        @media (min-width: 601px) {
          .mobile-bottom-nav {
            display: none !important;
          }
        }
'''

# Mobile header HTML to add
mobile_header_html = '''
    <!-- Add premium brand header for mobile -->
    <div class="brand-header-mobile d-block d-sm-none" style="background: #fff; box-shadow: 0 8px 24px rgba(0,0,0,0.10); padding: 1.5rem 0 1rem 0; text-align: center; position: relative; border-radius: 0 0 18px 18px; overflow: hidden; display: flex; align-items: center; justify-content: space-between; flex-direction: column; width: 100%; max-width: 100vw;">
      <div style="position: absolute; top: 0; left: 0; width: 100%; height: 7px; background: linear-gradient(90deg, #ffd600 0%, #fff700 100%); z-index: 2;"></div>
                 <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; padding: 0 8px; box-sizing: border-box;">
               <span class="header-brand-premium" style="flex: 1; font-family: 'Poppins', 'Montserrat', Arial, sans-serif; font-size: 1.7rem; font-weight: 900; letter-spacing: 2.5px; text-transform: uppercase; color: #0d47a1; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 48px; white-space: nowrap; position: relative; text-shadow: 0 2px 12px #90caf9, 0 1px 0 #fff, 0 0 8px #1976d2aa; margin-right: 8px;">RAJ SHREE MINERAL
                   <span style="display: block; width: 44px; height: 4px; background: linear-gradient(90deg, #ffd600 0%, #fff700 100%); border-radius: 2px; margin-top: 4px;"></span>
                   <span id="goldenArrow" style="display: block; width: 44px; height: 0; position: relative; cursor: pointer;">
                       <span style="position: absolute; left: 50%; transform: translateX(-50%); top: 0; width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-top: 8px solid #ffd600;"></span>
                   </span>
               </span>
               <span style="display: inline-block; width: 12px; height: 4px; background: linear-gradient(90deg, #ffd600 0%, #fff700 100%); border-radius: 2px; margin-right: 4px; flex-shrink: 0;"></span>
               <button class="nav-toggle" id="mobileMenuBtn" aria-label="Toggle menu" style="background: none; border: none; outline: none; padding: 4px; font-size: 2.1rem; color: #0d47a1; display: flex !important; align-items: center; cursor: pointer; z-index: 9999 !important; pointer-events: auto; position: relative; min-width: 44px; min-height: 44px; justify-content: center; flex-shrink: 0;">
                   <i class="fa fa-bars" id="menuIcon"></i>
               </button>
            </div>
      <div style="width: 50%; height: 7px; background: linear-gradient(90deg, #ffd600 0%, #fff700 100%); border-radius: 3.5px; margin-left: 0; margin-top: 8px;"></div>
    </div>
'''

# Mobile sidebar HTML template
def get_sidebar_html(active_page):
    """Generate sidebar HTML with the correct active page"""
    pages = {
        'index.html': 'Home',
        'about.html': 'About', 
        'products.html': 'Products',
        'applications.html': 'Applications',
        'infrastructure.html': 'Infrastructure',
        'contact.html': 'Contact'
    }
    
    sidebar_html = '''
    <!-- Premium Sidebar structure -->
    <div id="mobileSidebar" class="sidebar">
      <div class="close-btn" onclick="toggleSidebar()">✕</div>
      <ul class="sidebar-links">
'''
    
    for page, name in pages.items():
        if page == active_page:
            sidebar_html += f'        <li class="active"><a href="{page}"><i class="fas fa-{"home" if page == "index.html" else "info-circle" if page == "about.html" else "box" if page == "products.html" else "cogs" if page == "applications.html" else "building" if page == "infrastructure.html" else "envelope"}"></i> {name}</a></li>\n'
        else:
            sidebar_html += f'        <li><a href="{page}"><i class="fas fa-{"home" if page == "index.html" else "info-circle" if page == "about.html" else "box" if page == "products.html" else "cogs" if page == "applications.html" else "building" if page == "infrastructure.html" else "envelope"}"></i> {name}</a></li>\n'
    
    sidebar_html += '''      </ul>
      <div class="social-icons">
        <a href="https://instagram.com/rajshreemineral" target="_blank"><i class="fab fa-instagram"></i></a>
        <a href="https://wa.me/919427101391" target="_blank"><i class="fab fa-whatsapp"></i></a>
        <a href="mailto:rajshreemineral@gmail.com"><i class="fas fa-envelope"></i></a>
      </div>
    </div>
    <div id="sidebarBackdrop" onclick="toggleSidebar()"></div>
'''
    return sidebar_html

# JavaScript to add
sidebar_javascript = '''
      // Mobile sidebar functionality
      window.onload = function() {
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const goldenArrow = document.getElementById('goldenArrow');
        const menuIcon = document.getElementById('menuIcon');
        
        // Golden arrow click handler
        if (goldenArrow) {
          goldenArrow.addEventListener('click', function(e) {
            e.stopPropagation();
            console.log('Golden arrow clicked');
            toggleSidebar();
          });
        }
        
        // Menu button click handler
        if (mobileMenuBtn) {
          mobileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            console.log('Menu button clicked');
            toggleSidebar();
          });
        }
      };

      // Sidebar toggle function
      function toggleSidebar() {
        const sidebar = document.getElementById('mobileSidebar');
        const backdrop = document.getElementById('sidebarBackdrop');
        sidebar.classList.toggle('show');
        backdrop.classList.toggle('show');
        if ("vibrate" in navigator) navigator.vibrate(30); // Haptic feedback
      }
'''

def update_file(filename):
    """Update a single HTML file with mobile sidebar"""
    print(f"Updating {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has mobile sidebar
        if 'mobileSidebar' in content:
            print(f"  {filename} already has mobile sidebar, skipping...")
            return
        
        # Add CSS to the style section
        if '<style>' in content:
            # Find the last </style> tag and add CSS before it
            style_end = content.rfind('</style>')
            if style_end != -1:
                content = content[:style_end] + mobile_sidebar_css + content[style_end:]
        
        # Add mobile header before the first header or body content
        body_start = content.find('<body')
        if body_start != -1:
            body_content_start = content.find('>', body_start) + 1
            content = content[:body_content_start] + mobile_header_html + content[body_content_start:]
        
        # Add sidebar HTML before the closing body tag
        body_end = content.rfind('</body>')
        if body_end != -1:
            sidebar_html = get_sidebar_html(filename)
            content = content[:body_end] + sidebar_html + content[body_end:]
        
        # Add JavaScript before the closing script tag
        script_end = content.rfind('</script>')
        if script_end != -1:
            content = content[:script_end] + sidebar_javascript + content[script_end:]
        
        # Write back to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ {filename} updated successfully!")
        
    except Exception as e:
        print(f"  ✗ Error updating {filename}: {e}")

def main():
    """Main function to update all files"""
    print("Starting mobile sidebar update for all pages...")
    
    for filename in html_files:
        if os.path.exists(filename):
            update_file(filename)
        else:
            print(f"  ✗ {filename} not found, skipping...")
    
    print("\nUpdate complete! All pages now have the mobile sidebar.")

if __name__ == "__main__":
    main() 