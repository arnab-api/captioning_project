
-- pragma table_info(caption_site_captionmodel);
-- pragma table_info(caption_site_image);


-- delete from caption_site_caption
--     where id < 20;

-- insert into caption_site_presetopinionoption(opinion, is_positive)
--     values("The caption does not have sufficient details, but it is okay to understand the image", True);

-- select * from  caption_site_feedback2presetopinion
--     where opinion_id = 22;

-- update caption_site_feedback2presetopinion
--     set opinion_id = 22
--     where opinion_id = 20;

-- pragma table_info(caption_site_feedback);

-- insert into caption_site_image(human_annotation, image)
--     values(
--         "Three people sit at a picnic table outside of a building painted like a union jack", 
--         "images/caption_site/1258913059_07c613f7ff.png"
--     );

-- delete from caption_site_feedback;
-- delete from caption_site_caption;
-- delete from caption_site_captionmodel;
-- delete from caption_site_feedback;
-- delete from caption_site_feedback2presetopinion;
-- delete from caption_site_image;
-- delete from caption_site_presetopinionoption;

-- pragma table_info(caption_site_captionmodel);
-- insert into caption_site_captionmodel(model_name, description, url)
--     values(
--         "Microsoft Caption Bot", 
--         "N/A", 
--         "https://www.google.com/"
--     );

select * from caption_site_caption

-- 15 16 >> 15
-- update caption_site_presetopinionoption
--     set opinion = "The caption does not mention or incorrectly mentions the color of the person(s), or animal(s), or object(s) in the image"
--     where id = 15;

-- select * from caption_site_feedback2presetopinion
-- where opinion_id = 15;

-- update caption_site_feedback2presetopinion
--     set opinion_id = 15
--     where opinion_id = 16;
-- 206, 238

-- delete from caption_site_feedback2presetopinion
-- where id = 206 or id = 238;

-- delete from caption_site_presetopinionoption
--     where id = 16;
