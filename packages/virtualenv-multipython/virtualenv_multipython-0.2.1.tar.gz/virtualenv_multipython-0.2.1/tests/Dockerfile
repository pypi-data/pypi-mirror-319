FROM makukha/multipython:unsafe

COPY . /test
WORKDIR /test

RUN <<EOT
    # remove version pre-installed with multipython
    python -m pip uninstall -y tox virtualenv-multipython
EOT

ARG TOX_TAG
ARG VIRTUALENV_PIN
RUN <<EOT
    set -eEux -o pipefail
    # install tox and current plugin version
    $(py bin --path "$TOX_TAG") -m pip install tox "virtualenv$VIRTUALENV_PIN" .
EOT
# turn the plugin on
ENV VIRTUALENV_DISCOVERY=multipython

ARG TAGS_FAILING
RUN <<EOT
    set -eEux -o pipefail
    export RUNTOX="$(py bin --path "$TOX_TAG") -m tox"
    export ENVS_FAILING="$(sed 's/ /,/g' <<<"$TAGS_FAILING")"
    export ENVS_PASSING="$(py ls --tag | sed "s/$/  $TAGS_FAILING /; /^\(\S\+\) .* \1 /d; s/ .*//" | xargs | sed 's/ /,/g')"

    # test
    $RUNTOX -c tests/tox.ini run -m passing
    for TAG in $TAGS_FAILING; do
      [[ "$($RUNTOX -c tests/tox.ini run -e $TAG)" == "$TAG: failed with could not find"* ]]
    done
EOT
