function init() {

    echo "Initializing H2OGPT Mistral environment"
    export DATA_HOME=~/h2ogpt_mistral
    export CONTEXT_LENGTH=16384
    export IMAGE_TAG=f2be3591

    mkdir -p ${DATA_HOME}/.cache
    mkdir -p ${DATA_HOME}/save
    mkdir -p ${DATA_HOME}/user_path
    mkdir -p ${DATA_HOME}/db_dir_UserData
    mkdir -p ${DATA_HOME}/users
    mkdir -p ${DATA_HOME}/db_nonusers
    mkdir -p ${DATA_HOME}/auth
    mkdir -p ${DATA_HOME}/assets

    # copy auth files to ${DATA_HOME}/auth
    [ "$(ls -A ${DATA_HOME}/auth)" ] && cp -r ./h2ogpt_auth/* ${DATA_HOME}/auth
    [ "$(ls -A ${DATA_HOME}/assets)" ] && cp -r ./h2ogpt_assets/* ${DATA_HOME}/assets
}

function start_h2ogpt() {

    echo "Starting H2OGPT Mistral"
    docker run \
    --detach --init \
    --name h2ogpt_mistral \
    --restart=unless-stopped \
    --gpus all \
    --runtime=nvidia \
    --shm-size=2g \
    -p 7860:7860 \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -u $(id -u):$(id -g) \
    -v "${HOME}"/h2ogpt_mistral/.cache:/workspace/.cache \
    -v "${HOME}"/h2ogpt_mistral/save:/workspace/save \
    -v "${HOME}"/h2ogpt_mistral/user_path:/workspace/user_path \
    -v "${HOME}"/h2ogpt_mistral/db_dir_UserData:/workspace/db_dir_UserData \
    -v "${HOME}"/h2ogpt_mistral/users:/workspace/users \
    -v "${HOME}"/h2ogpt_mistral/db_nonusers:/workspace/db_nonusers \
    -v "${HOME}"/h2ogpt_mistral/auth:/workspace/auth \
    -v "${HOME}"/h2ogpt_mistral/assets:/workspace/assets \
    gcr.io/vorvan/h2oai/h2ogpt-runtime:$IMAGE_TAG /workspace/generate.py \
    --page_title="GenNet AI" \
    --favicon_path="/workspace/assets/gennet_logo.svg" \
    --height=700 \
    --gradio_size="medium" \
    --h2ocolors=False \
    --avatars=False \
    --visible_h2ogpt_logo=False \
    --visible_h2ogpt_links=False \
    --visible_h2ogpt_qrcode=False \
    --visible_chatbot_label=False \
    --visible_system_tab=False \
    --visible_models_tab=False \
    --visible_expert_tab=False \
    --visible_login_tab=False \
    --enable_heap_analytics=False \
    --document_choice_in_sidebar=True \
    --actions_in_sidebar=True \
    --auth_access='closed' \
    --openai_server=False \
    --auth="/workspace/auth/users.json" \
    --h2ogpt_api_keys="/workspace/auth/api_keys.json" \
    --use_gpu_id=False \
    --score_model=None \
    --prompt_type=open_chat \
    --base_model=TheBloke/openchat_3.5-16k-AWQ \
    --compile_model=True \
    --use_cache=True \
    --use_flash_attention_2=True \
    --attention_sinks=True \
    --sink_dict="{'num_sink_tokens': 4, 'window_length': $CONTEXT_LENGTH }" \
    --save_dir='/workspace/save/' \
    --user_path='/workspace/user_path/' \
    --langchain_mode="UserData" \
    --langchain_modes="['UserData', 'LLM']" \
    --visible_langchain_actions="['Query']" \
    --visible_langchain_agents="[]" \
    --use_llm_if_no_docs=True \
    --max_seq_len=$CONTEXT_LENGTH \
    --enable_ocr=True \
    --enable_tts=False \
    --enable_stt=False

}


function start_api() {
    echo "Starting GennetAI API"
    docker compose -f api/docker-compose.yml up -d
}



function stoop_all() {
    echo "Stopping H2OGPT Mistral"
    echo "Stopping GennetAI API"
    docker stop h2ogpt_mistral
	docker rm h2ogpt_mistral # we need so later we can start it again with same name
    docker compose -f api/docker-compose.yml down
}


# parse command line arguments
# take only 2 options: start and stop

if [ "$1" == "start" ]; then
    init
    start_h2ogpt
    start_api
    elif [ "$1" == "stop" ]; then
    stoop_all
else
    echo "Usage: $0 {start|stop}"
    exit 1
fi
