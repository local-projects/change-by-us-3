define ["underscore", 
        "backbone", 
        "jquery", 
        "template", 
        "abstract-view",
        "model/UserModel",
        "model/ProjectModel"], 
    (_, 
     Backbone, 
     $, 
     temp, 
     AbstractView,
     UserModel,
     ProjectModel) ->

            CBUStripeEdit = AbstractView.extend
                
                initialize: (options_) ->
                    AbstractView::initialize.call @, options_
                    @user = new UserModel({id:@model.sid})
                    @user.fetch
                        success: =>@getProject()


                render: ->
                    @$el = $("<div class='content-wrapper clearfix'/>") 
                    @$el.template @templateDir+"/templates/partials-universal/stripe-form.html",
                        data: {account_id:@user.id , project_id:@project.id , name:@project.get("name")}, => @onTemplateLoad()
                    $(@parent).append @$el
                
                ### EVENTS ---------------------------------------------###
                onTemplateLoad:->
                    $form = @$el.find('form')
                    options =
                        success: (response_) =>
                            @onSuccess response_.data
                    $form.ajaxForm options

                    AbstractView::onTemplateLoad.call @

                onSuccess:(data_)-> 
                    @$el.html("")
                    @$el.template @templateDir+"/templates/partials-universal/stripe-review.html",
                        data: data_,  =>

                ### GETTER ---------------------------------------------###
                getProject:->
                    @project = new ProjectModel({id:@model.id})
                    @project.fetch
                        success: =>@render()