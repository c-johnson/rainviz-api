class RainController < ApplicationController
  API_KEY = "65209f6bd8f0408da3dad1cc1693f0d1"
  PROJECT_ID = 28444
  SPIDER_NAME = "calirain"

  def get_rain
    response = get_jobs(1)
    concat_id = response["jobs"][0]["id"]
    item_response = get_items_from_job(concat_id)
    new_item_response = []

    item_response.each do |item|
      item["precipValues"].each do |precipValue|
        precip = precipValue[1].strip
        if precip != "T" && precip != "0.00" && precip != "+"
          new_item_response.push(item)
        end
      end
    end

    result = new_item_response.uniq

    respond_to do |format|
      format.html  # index.html.erb
      format.json  { render :json => result }
      format.js { render :json => result, :callback => params[:callback] }
    end
  end

  private

  def get_items_from_job (concat_id)
    # URL is <scrapinghub>/items/:project_id/:spider_id/:job_id/stats
    # concat_id is <:project_id/:spider_id/:job_id> portion, for example  "id"=>"28444/2/24"

    params = {
      apikey: API_KEY,
      format: "json"
    }
    url = "https://storage.scrapinghub.com/items/#{concat_id}"
    response = RestClient.get url, {:params => params}
    return JSON.parse(response)
  end

  def get_jobs (num_jobs)
    params = {
      count: num_jobs,
      state: "finished",
      project: PROJECT_ID,
      apikey: API_KEY,
      spider: SPIDER_NAME
    }
    url = "https://dash.scrapinghub.com/api/jobs/list.json"
    response = RestClient.get url, {:params => params}
    return JSON.parse(response)
  end
end
