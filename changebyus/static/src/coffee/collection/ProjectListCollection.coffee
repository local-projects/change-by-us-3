define ["underscore", "backbone", "model/ProjectModel"], 
    (_, Backbone, ProjectModel) ->
        ProjectListCollection = Backbone.Collection.extend
            model: ProjectModel
            
            url: ->
                "/api/project/list?limit=6&sort=activity&order=desc"
            
            parse: (response_) ->
                if response_.success then response_.data else {}