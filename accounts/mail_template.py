def mail_template(header, message):
    template = '<!DOCTYPE html><html  xmlns = "http://www.w3.org/1999/xhtml"><head><meta http - equiv = "Content-Type" content = "text/html; charset=utf-8" /> \
    <meta name = "viewport" content = "width=device-width, initial-scale=1.0 " /><style type = "text/css"> \
    body { \
    -webkit - text - size - adjust: 100 % !important; \
    -ms - text - size - adjust: 100 % !important; \
    -webkit - font - smoothing: antialiased !important; \
    } \
    img \
    { \
        border: 0 !important; \
    outline: none !important; \
    } \
    p \
    { \
        Margin: 0px !important; \
    Padding: 0 \
    px !important; \
    } \
    table \
    { \
    border - collapse: collapse; \
    mso - table - lspace: 0px; \
    mso - table - rspace: 0px; \
    } \
    td, a, span \
    { \
    border - collapse: collapse; \
    mso - line - height - rule: exactly; \
    } \
    .ExternalClass * { \
        line - height: 100 %; \
    } \
    span.MsoHyperlink \
    { \
        mso - style - priority: 99; \
    color: inherit;} \
    span.MsoHyperlinkFollowed \
    { \
    mso - style - priority: 99; \
    color: inherit; \
    } \
    .em_gray \
    a \
    { \
        color:  # 333333; \
            text - decoration: none; \
    } \
    .em_gray1 \
    { \
        color:  # 808080; \
            text - decoration: none; \
    } \
    .em_gray1 \
    a \
    { \
        color:  # f06060; \
            text - decoration: none; \
    } \
    .em_gray1 \
    ul \
    { \
        margin: 0px; \
    padding: 0px; \
    list - style - position: inside; \
    list - style - type: disc; \
    } \
    .em_gray1 \
    ul \
    li \
    { \
        font: 14px  # 808080 Arial, sans-serif; \
        line - height: 20 \
    px; \
    margin: 0; \
    padding: 0; \
    } \
    .em_gray1 \
    ul \
    li \
    a \
    { \
        font: 14px  # 808080 Arial, sans-serif; \
         text - decoration: none; \
    } \
    .em_pink \
    a \
    { \
        color:  # f06060; \
            text - decoration: none; \
    } \
    .em_whte \
    a \
    { \
        color:  # ffffff; \
            text - decoration: none; \
    } \
    .em_white1 \
    a \
    { \
        color:  # f1f4f5; \
            text - decoration: none; \
    } \
    center \
    table \
    { \
        width: 100 % !important; \
    } \
 \
    @media \
 \
    only \
    screen and (min - width:481px) and (max - width:649px) \
    { \
        .em_wrapper \
    { \
        width: 100 % !important; \
    } \
    .em_hide \
    { \
        display: none !important; \
    } \
    .em_full_img \
    { \
        width: 100 % !important; \
    height: auto !important; \
    max - width: 100 % !important; \
    } \
    .em_pad_top \
    { \
        padding - top: 20px !important; \
    } \
    .em_pad_bottom \
    { \
        padding - bottom: 20px !important; \
    } \
    .em_height \
    { \
        height: 20px !important; \
    } \
    .em_space \
    { \
        width: 15px !important; \
    } \
    .em_wrapper_50_1 \
    { \
        width: 50 % !important; \
    max - width: none !important; \
    } \
    .em_center \
    { \
        text - align: center !important; \
    } \
    } \
 \
    @media \
 \
    only \
    screen and (max - width:480px) \
    { \
        .em_wrapper \
    { \
        width: 100 % !important; \
    } \
    .em_hide \
    { \
        display: none !important; \
    } \
    .em_full_img \
    { \
        width: 100 % !important; \
    height: auto !important; \
    max - width: 100 % !important; \
    } \
    .em_pad_top \
    { \
        padding - top: 20px !important; \
    } \
    .em_pad_bottom \
    { \
        padding - bottom: 20px !important; \
    } \
    .em_height \
    { \
        height: 20px !important; \
    } \
    .em_space \
    { \
        width: 15px !important; \
    } \
    .em_white \
    { \
        height: 20px !important; \
    background - color:  \
    # ffffff !important; \
    } \
    .em_center \
    { \
        text - align: center !important; \
    } \
    .em_wrapper_50_1 \
    { \
        width: 50 % !important; \
    max - width: none !important; \
    } \
    } \
    </ style> \
    <!--[ if gte \
    mso \
    9]> \
    <style> \
    ul \
    { \
        margin: 0 0 0 30px !important; \
    padding: 0 !important; \
    list - style - position: inside; \
    } \
    ul \
    li \
    { \
        font: 14px  # 808080 Arial, sans-serif; \
        color:  # 808080 !important; \
    text - decoration:none !important; \
    margin: 0 \
    0 \
    0 \
    30 \
    px; \
    padding: 0; \
    list - style: disc; \
 \
    } \
    ul \
    li \
    a \
    { \
        font: 14px  # 808080 Arial, sans-serif; \
        color:  # 808080 !important; \
    text - decoration:none !important; \
    line - height: 20 \
    px; \
 \
    } \
    </style>' + '</head> \
    <body style = "margin: 0px;padding: 0px;-webkit-text-size-adjust: 100% !important;-ms-text-size-adjust: 100% !important;-webkit-font-smoothing: antialiased !important;" \
    bgcolor = "#ffffff"> \
    <table width = "100%" border = "0" align = "center" cellspacing = "0" cellpadding = "0" bgcolor = "#ffffff" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr><td align = "center" valign = "top" style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table style = "table-layout: fixed;border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;" \
    width = "650" border = "0" cellspacing = "0" cellpadding = "0" align = "center" class ="em_wrapper"> \
    <tr> \
    <td class ="em_hide" height="1" style="line-height: 0px;font-size: 0px;border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <img src="images/spacer.gif" height="1" alt="" width="650" style="display: block;width: 650px;min-width: 650px;border: 0 !important;outline: none !important;" border="0" /> </td> \
    </tr><tr><br /><br />' + '<td \
    class ="em_bg_grey" valign="top" style="border-collapse: collapse;mso-line-height-rule: exactly;background-color: #333333;"> \
    <table width = "650" border = "0" cellspacing = "0" cellpadding = "0" align = "center" \
    class ="em_wrapper" style="border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td height = "36" \
    class ="em_height" style="border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <img src="images/spacer.gif" width="1" height="1" alt="" style="display:block;" border="0" /> </ td> \
  </ tr> \
    <tr> \
    <td \
    align = "center" \
    valign = "top" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "650" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
    width = "30" \
 \
    class ="hide" style="border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <img src="images/spacer.gif" width="1" height="1" alt="" style="display:block;" border="0" /> </ td> \
 \
    <td \
    align = "center" \
    valign = "top" \
    style = "font-size: 0px;line-height: 0px;border-collapse: collapse;mso-line-height-rule: exactly;"> <span \
    style = "display: block;max-width: 200px;font-family: Arial, sans-serif;font-size: 20px;line-height: 16px;color: #ffffff;font-weight: bold;border: 0 !important;outline: none !important;"> BrandFactory \
    Inc </ span> </ td> \
    <td \
    width = "30" \
 \
    class ="hide" style="border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <img src="images/spacer.gif" width="1" height="1" alt="" style="display:block;" border="0" /> </ td> \
 \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
    <tr> \
    <td \
    height = "36" \
 \
    class ="em_height" style="border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <img src="images/spacer.gif" width="1" height="1" alt="" style="display:block;" border="0" /> </ td> \
 \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
 \
    </ table> \
    <br /> \
 \
    <table \
    width = "100%" \
    border = "0" \
    align = "center" \
    cellspacing = "0" \
    cellpadding = "0" \
    bgcolor = "#ffffff" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td \
    valign = "top" \
    align = "center" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "650" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="table-layout: fixed;border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
    align = "center" \
    valign = "top" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "50" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td \
    height = "2" \
    style = "line-height: 0px;font-size: 0px;border-collapse: collapse;mso-line-height-rule: exactly;background-color: #6e9dea;" \
 \
    class ="em_bg_pink"> </ td> \
 \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
    </ table> \
    <br /> \
    <br /> \
 \
    <table \
    width = "100%" \
    border = "0" \
    align = "center" \
    cellspacing = "0" \
    cellpadding = "0" \
    bgcolor = "#ffffff" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td \
    valign = "top" \
    align = "center" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "650" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="table-layout: fixed;border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
    width = "45" \
 \
    class ="em_space" style="border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
 \
    <td \
    valign = "top" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "100%" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td \
 \
    class ="em_gray" align="center" style="border-collapse: collapse;mso-line-height-rule: exactly;color: #333333;font-family: Arial, sans-serif;font-size: 24px;line-height: 27px;text-decoration: none;">' + header + '</ td> \
 \
    </ tr> \
    <tr> \
    <td \
    height = "7" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
    </ tr> \
    <tr> \
    <td \
 \
    class ="em_gray" align="center" style="border-collapse: collapse;mso-line-height-rule: exactly;color: #333333;font-family: Arial, sans-serif;font-size: 14px;line-height: 17px;text-decoration: none;">' + message + '</ td> \
 \
    </ tr> \
    <tr> \
    <td \
    height = "15" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
    </ tr> \
    </ table> \
    </ td> \
    <td \
    width = "45" \
 \
    class ="em_space" style="border-collapse: collapse;mso-line-height-rule: exactly; font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
 \
    </ table> \
    </ td> \
    </ tr> \
    </ table> \
    <table \
    width = "100%" \
    border = "0" \
    align = "center" \
    cellspacing = "0" \
    cellpadding = "0" \
    bgcolor = "#ffffff" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td \
    valign = "top" \
    align = "center" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "650" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="table-layout: fixed;border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
    height = "2" \
    style = "line-height: 0px;font-size: 0px;border-collapse: collapse;mso-line-height-rule: exactly;background-color: #6e9dea;" \
 \
    class ="em_bg_pink"> </ td> \
 \
    </ tr> \
    <tr> \
    </ table> \
    </ td> \
    </ tr> \
    </ table> \
    <br /> \
    <br /> \
    <table \
    width = "100%" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td \
    valign = "top" \
    align = "center" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "650" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="table-layout: fixed;border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
 \
    class ="em_bg_grey" style="border-collapse: collapse;mso-line-height-rule: exactly;background-color: #333333;"> \
 \
    <table \
    width = "650" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
    height = "35" \
 \
    class ="em_height" style="border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
 \
    </ tr> \
    <tr> \
    <td \
    align = "center" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "650" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
    width = "100" \
 \
    class ="em_space" style="border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
 \
    <td \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "450" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
 \
    class ="em_wrapper" style="border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
 \
    <tr> \
    <td \
 \
    class ="em_gray1" align="center" style="border-collapse: collapse;mso-line-height-rule: exactly;color: #808080;font-family: Arial, sans-serif;font-size: 12px;line-height: 20px;text-decoration: none;"> \
 \
    Copyright & copy; \
    2019, All \
    rights \
    reserved \
    at \
    BrandFactory \
    Inc \
    </ td> \
    </ tr> \
    <tr> \
    <td \
    height = "20" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
    </ tr> \
    <tr> \
    <td \
 \
    class ="em_gray1" align="center" style="border-collapse: collapse;mso-line-height-rule: exactly;color: #808080;font-family: Arial, sans-serif;font-size: 12px;line-height: 20px;text-decoration: none;"> <span class ="em_pink"> <a href="#" target="_blank" style="color: #6e9dea;text-decoration: none;white-space: nowrap;border-collapse: collapse;mso-line-height-rule: exactly;"> Unsubscribe from this list </ a> </ span> <span class ="em_hide" style="border-collapse: collapse;mso-line-height-rule: exactly;"> </ span> </ td> \
 \
    </ tr> \
    <tr> \
    <td \
    height = "20" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
    </ tr> \
    <tr> \
    <td \
    align = "center" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> \
    <table \
    width = "92" \
    border = "0" \
    cellspacing = "0" \
    cellpadding = "0" \
    align = "center" \
    style = "border-collapse: collapse;mso-table-lspace: 0px;mso-table-rspace: 0px;"> \
    <tr> \
    <td \
    width = "24" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> <a \
    href = "https://facebook.com/" \
    target = "_blank" \
    style = "text-decoration: none;border-collapse: collapse;mso-line-height-rule: exactly;"> <img \
    src = "images/facebook2.png" \
    width = "24" \
    height = "24" \
    alt = "Fb" \
    style = "display: block;border: 0 !important;outline: none !important;" \
    border = "0"> </ a> </ td> \
    <td \
    width = "10" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
    <td \
    width = "24" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> <a \
    href = "https://twitter.com/" \
    target = "_blank" \
    style = "text-decoration: none;border-collapse: collapse;mso-line-height-rule: exactly;"> <img \
    src = "images/twitter2.png" \
    width = "24" \
    height = "24" \
    alt = "Tw" \
    style = "display: block;border: 0 !important;outline: none !important;" \
    border = "0"> </ a> </ td> \
    <td \
    width = "10" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
    <td \
    width = "24" \
    style = "border-collapse: collapse;mso-line-height-rule: exactly;"> <a \
    href = "#" \
    target = "_blank" \
    style = "text-decoration: none;border-collapse: collapse;mso-line-height-rule: exactly;"> <img \
    src = "images/google_plus.png" \
    width = "24" \
    height = "24" \
    alt = "G+" \
    style = "display: block;border: 0 !important;outline: none !important;" \
    border = "0"> </ a> </ td> \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
    </ table> \
    </ td> \
    <td \
    width = "100" \
 \
    class ="em_space" style="border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
 \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
    <tr> \
    <td \
    height = "35" \
 \
    class ="em_height" style="border-collapse: collapse;mso-line-height-rule: exactly;font-size:0px; line-height:0px;"> <br /> <br /> </ td> \
 \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
    </ table> \
    </ td> \
    </ tr> \
    </ table> \
    <!-- == = // FOOTER_SECTION_3 == = --> \
    </ td> \
    </ tr> \
    </ table> \
    <!-- == = // FOOTER \
    SECTION == = --> \
    <div \
    style = "display:none; white-space:nowrap; font:20px courier; color:#ffffff; background-color:#ffffff;"> & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; </ div> \
    <custom \
    name = "opencounter" \
    type = "tracking" /> \
    </ body> \
    </ html>'

    return template
