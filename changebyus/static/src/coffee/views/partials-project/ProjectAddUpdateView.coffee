define ["underscore", 
        "backbone", 
        "jquery", 
        "template", 
        "abstract-view", 
        "project-sub-view",
        "views/partials-universal/WysiwygFormView",
        "views/partials-universal/UpdateListItemView",
        "views/partials-project/ProjectUpdateSuccessModalView"],
    (_, 
     Backbone, 
     $, 
     temp, 
     AbstractView, 
     ProjectSubView, 
     WysiwygFormView, 
     UpdateListItemView, 
     ProjectUpdateSuccessModalView) ->

        ProjectAddUpdateView = ProjectSubView.extend

            parent: "#project-update"
            linkingSite: ""

            events: 
                "click #post-update":"animateUp"
                "click .share-toggle":"shareToggle"
                "click .share-options .styledCheckbox":"shareOption"

            render: -> 
                @viewData.image_url_round_small = $('.profile-nav-header img').attr('src')
                self = @
                @$el = $(@parent)
                @$el.template @templateDir+"partials-project/project-add-update.html",
                    {data: @viewData}, => @onTemplateLoad()

                # set global function that gets called from popup window
                document.windowReload = -> self.getSocial(false)

            onTemplateLoad:-> 
                @$ul = @$el.find('.updates-container ul')
                
                @getSocial()

                ProjectSubView::onTemplateLoad.call @

            getSocial:(addForm_=true)->
                # check to see if social accounts are linked and hide the share options if they aren't
                $.get "/api/user/socialinfo", (response_)=>
                    try
                        @socialInfo = response_.data
                        if addForm_ then @addForm() else @checkSocial(true)
                    catch e
                        console.log 'getSocial ERROR:', e

            shareToggle:->
                $(".share-options").toggleClass("hide")

            shareOption:(e)->
                checked = []
                $.each $('.share-options input'), ->
                    $this = $(this)
                    id = $this.attr('id')
                    if ($this.is(':checked')) then checked.push id
                         
                $('#social_sharing').val checked.join()

            addForm:->
                form = new WysiwygFormView({parent:"#update-form"})
                form.on 'ON_TEMPLATE_LOAD', =>  
                    $feedback       = $("#feedback").hide()
                    $submit         = form.$el.find('input[type="submit"]')
                    $inputs         = $submit.find("input, textarea")
                    @$facebook      = $("#facebook")
                    @$twitter       = $("#twitter")
                    @$facebookLabel = $("label[for=facebook]")
                    @$twitterLabel  = $("label[for=twitter]")
                    
                    form.beforeSubmit = (arr_, form_, options_)-> 
                        $feedback.hide()
                        $inputs.attr("disabled", "disabled")

                    form.success = (response_)=> 
                        if response_.success
                            @addModal response_.data

                        form.resetForm()
                        $("#editor").html("")
                        $inputs.removeAttr("disabled")

                    form.error = (error_)=>
                        $feedback.show() 

                    @$el.find('input:radio, input:checkbox').screwDefaultButtons
                        image: 'url("/static/img/black-check.png")'
                        width: 18
                        height: 18

                    @checkSocial()
                    @delegateEvents()

            checkSocial:(forceClick_=false)->
                # check to see if user has linked social accounts 
                # and see if it originated from clicking an unactive label or checkbox

                if @socialInfo.fb_name is ""
                    @$facebook.screwDefaultButtons("disable")
                    @$facebook.parent().click ()=> @socialClick("facebook")
                    @$facebookLabel.addClass("disabled-btn").click ()=> @socialClick("facebook")
                else
                    @$facebook.screwDefaultButtons("enable")
                    if forceClick_ and @linkingSite is "facebook" then @$facebook.screwDefaultButtons("check")
                    @$facebookLabel.removeClass("disabled-btn").unbind "click"

                if @socialInfo.twitter_name is ""
                    @$twitter.screwDefaultButtons("disable")
                    @$twitter.parent().click ()=> @socialClick("twitter")
                    @$twitterLabel.addClass("disabled-btn").click ()=> @socialClick("twitter")
                else
                    @$twitter.screwDefaultButtons("enable")
                    if forceClick_ and @linkingSite is "twitter" then @$twitter.screwDefaultButtons("check")
                    @$twitterLabel.removeClass("disabled-btn").unbind "click"

            animateUp:->
                $("html, body").animate({ scrollTop: 0 }, "slow")

            socialClick:(site_)->
                @linkingSite = site_
                popWindow "/social/#{site_}/link"

            # ATTACH ELEMENTS 
            # -----------------------------------------------------------------
            addAll: ->   
                @$day = $('<div />')
                @$day.template @templateDir+"partials-universal/entries-day-wrapper.html",
                    {}, => @onDayWrapperLoad()

            onDayWrapperLoad: ->
                ProjectSubView::onDayWrapperLoad.call(@)
                ProjectSubView::addAll.call(@) 

                onPageElementsLoad()

            # use parent method 
            # newDay:(date_)->
                    
            addOne: (model_) ->
                m = moment(model_.get("created_at")).format("MMMM D")
                if @currentDate isnt m then @newDay(m) 

                view = new UpdateListItemView({model: model_})
                @$ul.append view.$el 

            addModal:(data_)-> 
                data_.twitter_name = @socialInfo.twitter_name
                data_.slug         = @model.get("slug")
                modal              = new ProjectUpdateSuccessModalView({model:data_})
